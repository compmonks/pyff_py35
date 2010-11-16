__copyright__ = """ Copyright (c) 2010 Torsten Schmits

This program is free software; you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation; either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <http://www.gnu.org/licenses/>.
"""

from time import sleep
from itertools import count

from AlphaBurst.model.character_sequence import CharacterSequenceFactory

__all__ = ['CountExperiment', 'YesNoExperiment', 'CopySpellingExperiment',
           'CalibrationExperiment', 'FreeSpellingExperiment']

class Experiment(object):
    def __init__(self, view, trial, input_handler, flag, iter, alphabet,
                 palette, config):
        self._view = view
        self._trial = trial
        self._input_handler = input_handler
        self._flag = flag
        self._iter = iter
        self._alphabet = alphabet
        self._palette = palette
        self._redundance = config.meaningless
        self._words = config.words
        self._inter_trial = config.inter_trial
        self._alternating_colors = config.alternating_colors
        self._sequences_per_trial = config.sequences_per_trial
        self._custom_pre_sequences = config.custom_pre_sequences
        self._custom_post_sequences = config.custom_post_sequences
        self._current_target = ''

    def trial(self):
        sleep(self._inter_trial)
        factory = CharacterSequenceFactory(self._redundance,
                                           self._alternating_colors,
                                           self._current_target,
                                           self._palette)
        sequences = factory.sequences(self._sequences_per_trial,
                                      self._custom_pre_sequences,
                                      self._custom_post_sequences)
        self._input_handler.start_trial(self._trial)
        self._trial.run(sequences)
        if self._flag:
            self._trial.evaluate(self._input_handler)

class GuidedExperiment(Experiment):
    def run(self):
        for word in self._iter(self._words):
            self._view.count_down()
            self._view.word(word)
            for target in enumerate(self._iter(word)):
                self.trial(*target)

    def trial(self, index, target):
        self._view.target(index)
        self._trial.target(target)
        Experiment.trial(self)

YesNoExperiment = GuidedExperiment
CopySpellingExperiment = GuidedExperiment
CalibrationExperiment = GuidedExperiment

class CountExperiment(GuidedExperiment):
    def trial(self, *a, **kw):
        self.detections = []
        GuidedExperiment.trial(self, *a, **kw)

class FreeSpellingExperiment(Experiment):
    def run(self):
        for i in self._iter(count()):
            self.trial()
