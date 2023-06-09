import logging
import random
import numpy as np


class BinaryGenetics:
    @staticmethod
    def _do_score_tournament(scores, rounds):
        assert type(rounds) is int, 'number of rounds in tournament should be integer'

        max_ind = random.randint(0, len(scores)-1)

        for r in range(0, max(0, rounds - 1)):
            r_num = random.randint(0, len(scores)-1)
            if scores[r_num] > scores[max_ind]:
                max_ind = r_num
        return max_ind

    def __init__(self,
                 n_samples=100,
                 n_generations=20,
                 save_best_n=1,
                 p_point_mutate=0.1,
                 top_n=None,
                 binary_shape=50,
                 inbreed_prob=0.1,
                 random_interchange_prob=0.1,
                 n_interchange_points=1,
                 tournament_rounds=2,
                 cached=True,
                 inbreed_distance_func=None,
                 logging_obj=None,
                 tqdm_obj=None):
        """
        BinaryGenetics optimizer class
        :param n_samples: number of samples in one generation
        :param n_generations: number of generations to run
        :param save_best_n: number of top species to be saved as-is from current generation
        :param p_point_mutate: probability to have at least one mutation in child after born
        :param binary_shape: shape of binary vector to optimize
        :param inbreed_prob: probability with which second parent is picked from most "closest" by
        inbreed_distance_func from samples
        :param random_interchange_prob: probability of non crossover child production, but when child randomly
        (with prob 0.5) gets parent genes
        :param tournament_rounds: int number of rounds in tournament. if 1 - then parents are selected randomly,
        if more, then algorithm become more selective
        :param n_interchange_points: number of crossover points
        :param cached: use internal caching for eval function
        :param inbreed_distance_func: function to check distance between two binary vectors for distance between them, l1 by default
        :param logging_obj: object, which is used for logging
        :param tqdm_obj: object used for progress bar  painting. If None, then no progress bar created
        """

        self.tournament_rounds = tournament_rounds
        self.n_interchange_points = n_interchange_points
        self.random_interchange_prob = random_interchange_prob
        self.n_samples = n_samples
        self.n_generations = n_generations
        self.save_best_n = save_best_n
        self.p_point_mutate = 1-np.power((1-p_point_mutate),1.0/binary_shape)
        if top_n is None:
            self.top_n = max(save_best_n+1,int(self.n_samples*0.2))
        else:
            self.top_n = max(save_best_n+1, int(top_n))
        self.best_samples = None
        self.best_scores = None
        self.binary_shape = binary_shape
        self._for_choice = [i for i in range(binary_shape)]
        self._cache = dict()
        self._cached = cached
        self._current_samples_hashes = set()

        # inbreed
        self.inbreed_prob = inbreed_prob
        self.inbreed_func = inbreed_distance_func
        self.inbreed_rank_probs = [np.exp(-1 - (1 / 10) * (x_)) for x_ in range(self.n_samples + 1)]

        if inbreed_distance_func is None:
            def default_inbreed_func(x, y):
                # l1 default
                return np.sum(np.abs(x.astype(np.int8) - y.astype(np.int8)))

            self.inbreed_func = default_inbreed_func

        if logging_obj is None:
            self.logging_obj = logging.info
        else:
            self.logging_obj = logging_obj
        self.tqdm_obj = tqdm_obj
        if self.tqdm_obj is None:
            self.tqdm_obj = lambda x: x

    def set_eval_func(self, eval_func, greater_is_better=True):
        '''
        Set evaluation func for binary vector
        :param eval_func: function with one argument: bunary vector. Function must return only one float number:
        quality (or score) of a child
        :param greater_is_better: if True, then optimization is targeted for maximizing
        :return: None
        '''
        self.eval_func = eval_func
        self.greater_is_better = greater_is_better

    def _call_eval_func(self, sample):
        if self._cached:
            sample_tuple = tuple([bool(s) for s in sample])
            if sample_tuple in self._cache:
                return self._cache[sample_tuple]
            value = self.eval_func(sample)
            self._cache[sample_tuple] = value
            return value
        return self.eval_func(sample)

    def _is_in_pop(self, sample):
        sample_tuple = tuple([bool(s) for s in sample])
        return sample_tuple in self._current_samples_hashes

    def _add_to_pop(self, sample):
        self._current_samples_hashes.add(tuple([bool(s) for s in sample]))

    def _clear_pop(self):
        self._current_samples_hashes.clear()

    def learn(self, yield_best=False, samples=None):
        '''
        Main method to start optimizing
        :param yield_best: create iterator fot best sample in generation
        :param samples: initial samples to start from
        :return: iterator, if yield_best is set to True, else list of best samples with according
        scores from each generation
        '''
        # initial samples
        if samples is None:
            samples = np.random.random((self.n_samples, self.binary_shape)) > 0.5

        current_gen = 0
        prev_saved = None
        while current_gen < self.n_generations:
            if type(prev_saved) is list:
                scores = np.array(prev_saved + [self._call_eval_func(samples[i]) for i in
                                                self.tqdm_obj(range(len(prev_saved), samples.shape[0]))])
                prev_saved.clear()
            else:
                scores = np.array([self._call_eval_func(samples[i]) for i in
                                   self.tqdm_obj(range(samples.shape[0]))])  # self.eval_func, 1, samples)
                prev_saved = list()


            if self.greater_is_better:
                best_ranks = np.argsort(scores)[::-1][:self.top_n]
            else:
                best_ranks = np.argsort(scores)[:self.top_n]
            sorted_scores = scores[best_ranks]

            self.logging_obj('Generation {} top score {} median score {}'.format(current_gen, sorted_scores[0],
                                                                                 np.median(sorted_scores)))

            self.best_scores = sorted_scores
            self.best_samples = samples[best_ranks, :]

            if yield_best:
                yield self.best_samples[0], self.best_scores[0]

            current_samples = 0
            samples = np.zeros((self.n_samples, self.binary_shape))

            while current_samples < self.n_samples:
                if current_samples < self.save_best_n:
                    samples[current_samples,:] = self.best_samples[current_samples]
                    self._add_to_pop(samples[current_samples])
                    prev_saved.append(self.best_scores[current_samples])
                    current_samples += 1
                    continue

                # do inbreed if probability to do so
                if np.random.random() < self.inbreed_prob:
                    # inbreed here
                    first_index = self._do_score_tournament(self.best_scores,self.tournament_rounds)
                    first_sample = self.best_samples[first_index]

                    # inbreed probability is not based on score, but on other "inbreed_func" value
                    other_scores = np.array([self.inbreed_func(first_sample, sample) for sample in self.best_samples])
                    second_index = self._do_score_tournament(other_scores,self.tournament_rounds)

                else:
                    # random choice acc to scores
                    first_index = self._do_score_tournament(self.best_scores, self.tournament_rounds)
                    second_index = self._do_score_tournament(self.best_scores, self.tournament_rounds)

                if np.random.random() < self.random_interchange_prob:
                    # random x-y interchange
                    for v in range(self.binary_shape):
                        samples[current_samples, v] = self.best_samples[first_index, v] if np.random.random() > 0.5 else \
                        self.best_samples[second_index, v]
                else:
                    # point-cross interchange
                    from_first_parent = True
                    interchange_points = set(
                        [random.choice(self._for_choice) for i in range(self.n_interchange_points)])

                    for v in range(self.binary_shape):
                        if v in interchange_points:
                            from_first_parent = not from_first_parent

                        samples[current_samples, v] = self.best_samples[first_index, v] if from_first_parent else \
                        self.best_samples[second_index, v]

                samples[current_samples] = self.mutate_sample(samples[current_samples])# if sample is already in population

                if self._is_in_pop(samples[current_samples]):
                    continue

                self._add_to_pop(samples[current_samples])
                current_samples += 1

            self._clear_pop()
            samples = samples.astype(bool)
            current_gen += 1

        return self.best_samples, self.best_scores

    def mutate_sample(self, sample):
        '''
        # Mutate sample. Probability to get non mutated is (1-self.p_point_mutate)
        :param sample:
        :return:
        '''
        for mutation_index,v in enumerate(sample):
            if np.random.random() < self.p_point_mutate:
                sample[mutation_index] = not v
        return sample