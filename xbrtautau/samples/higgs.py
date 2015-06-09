import yellowhiggs

from .sample import Sample
from .. import NTUPLE_PATH, DEFAULT_STUDENT
from .. import log; log = log[__name__]

class Signal(Sample):
    pass

class Higgs(Signal):

    MASSES = range(60, 205, 5)
    MODES = ['gg', 'VBF', 'Z']
    LEVELS = ['truth', 'reco']
    def __init__(self, e_com=13, 
                 mode=None, modes=None,
                 mass=None, masses=None,
                 level = None, levels = None,
                 ntuple_path=NTUPLE_PATH,
                 student=DEFAULT_STUDENT,
                 file_name = None,
                 suffix='_test',
                 label=None,
                 **kwargs):
        """
        Parameters
        ----------
        * e_com: LHC center-of-mass energy (13 or 8)
        * mass: Mass of the Higgs boson
        * mode: production mode (VBF/gg)
        """
        ## Adding reco level block --SINA

        if levels is None:
            if level is not None:
                assert level in Higgs.LEVELS
                levels = [level]
            else:
                levels = Higgs.LEVELS

        else:
            assert len(levels) > 0
            for level in levels:
                assert level in Higgs.LEVELS
            assert len(set(levels)) == len(levels)


        if masses is None:
            if mass is not None:
                assert mass in Higgs.MASSES
                masses = [mass]
            else:
                # default to 125
                masses = [125]
        else:
            assert len(masses) > 0
            for mass in masses:
                assert mass in Higgs.MASSES
            assert len(set(masses)) == len(masses)

        if modes is None:
            if mode is not None:
                assert mode in Higgs.MODES
                modes = [mode]
            else:
                # default to all modes
                modes = Higgs.MODES
        else:
            assert len(modes) > 0
            for mode in modes:
                assert mode in Higgs.MODES
            assert len(set(modes)) == len(modes)
            
        name = 'Signal'
#### --SINA
        str_level = ''
        if len(levels) == 1:
            str_level = levels[0]
            name += '_%s' % str_level

        
        str_mode = ''
        if len(modes) == 1:
            str_mode = modes[0]
            name += '_%s' % str_mode

        str_mass = ''
        if len(masses) == 1:
            str_mass = '%d' % masses[0]
            name += '_%s' % str_mass

        if label is None:
            label = '%s-%s#font[52]{H}(%s)#rightarrow#tau#tau' % (
                str_level, str_mode, str_mass)

        super(Higgs, self).__init__(name=name, label=label, **kwargs)
        self._sub_samples = []
        self._scales = []
        for level in levels:
            for mode in modes:
                for mass in masses:                    
                    self._sub_samples.append(Signal(
                            ntuple_path=ntuple_path, 
                            student='%s_%s_%s' % (level, mode, mass),
                            suffix=suffix,
                            level = level,
                            name='%s_Higgs_%s_%s' % (level, mode, mass), 
                            label='%s_Higgs_%s_%s' % (level, mode, mass)))
                    # Add all sample with a scale of 1
                    self._scales.append(1)


    @property
    def components(self):
        return self._sub_samples

    @property
    def scales(self):
        return self._scales


    def set_scales(self, scales):
        """
        """
        if isinstance(scales, (float, int)):
            for i in xrange(self._sub_samples):
                self._scales.append(scales)
        else:
            if len(scales) != len(self._sub_samples):
                log.error('Passed list should be of size {0}'.format(len(self._sub_samples)))
                raise RuntimeError('Wrong lenght !')
            else:
                for scale in scales:
                    self._scales.append(scale)
        
        log.info('Set samples scales: {0}'.format(self._scales))

 
    def draw_helper(self, *args, **kwargs):
        hist_array = []

        for s in self._sub_samples:
            h = s.draw_helper(*args)
            hist_array.append(h)

        if len(self._scales) != len(hist_array):
            log.error('The scales are not set properly')
            raise RuntimeError('scales need to be set before calling draw_helper')

        hsum = hist_array[0].Clone()
        hsum.reset()
        hsum.title = self.label

        for h, scale in zip(hist_array, self._scales):
            hsum += scale * h

        return hsum



