from .common import backend_test, plotting_test_with_plt, plotting_test_without_plt, non_syntetic_test
import regdata as rd

# Removing cached datasets
import os
os.system('rm /tmp/somerandomtexthere_*')

datasets = (
    rd.DellaGattaGene,
    rd.Heinonen4,
    rd.Jump1D,
    rd.MotorcycleHelmet,
    rd.NonStat2D,
    rd.Olympic,
    rd.SineJump1D,
    rd.SineNoisy,
    rd.Smooth1D,
    rd.Step,
)

def common(obj):
    backend_test(obj)
    plotting_test_with_plt(obj)
    plotting_test_without_plt(obj)
    if not obj().synthetic:
        non_syntetic_test(obj)

def test_common():
    for data in datasets:
        common(data)
