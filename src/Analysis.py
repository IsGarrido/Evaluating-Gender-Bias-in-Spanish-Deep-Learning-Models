from src import FileHelper
import matplotlib
matplotlib.use('module://backend_interagg')

mdata = FileHelper.pandad_read_tsv('../temp/m_7.tsv')
fdata = FileHelper.pandad_read_tsv('../temp/f_7.tsv')

mplot = mdata.plot(kind = 'box')
fdata.plot(kind = 'box')

