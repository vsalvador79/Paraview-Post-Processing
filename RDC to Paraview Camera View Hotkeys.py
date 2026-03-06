# Set 1: U/A/R/L/Shift+F/Shift+B  (A fixed with 180 roll)
from paraview.simple import *
import builtins

def fit_view(reset_fn, roll=None):
    v = GetActiveViewOrCreate("RenderView")
    v.Set(InteractionMode="Selection", CameraParallelProjection=1)
    reset_fn(v)
    v.ResetCamera(False, 0.9)
    if roll is not None:
        v.AdjustRoll(roll)
    Render(v)

def view_u():
    fit_view(lambda v: v.ResetActiveCameraToPositiveY())

def view_a():
    fit_view(lambda v: v.ResetActiveCameraToNegativeY(), roll=180.0)  # fixed

def view_r():
    fit_view(lambda v: v.ResetActiveCameraToNegativeX(), roll=90.0)

def view_l():
    fit_view(lambda v: v.ResetActiveCameraToPositiveX(), roll=-90.0)

def view_shift_f():
    fit_view(lambda v: v.ResetActiveCameraToNegativeZ())

def view_shift_b():
    fit_view(lambda v: v.ResetActiveCameraToPositiveZ())

def on_key(interactor, event):
    ks = (interactor.GetKeySym() or "").lower()
    shift = bool(interactor.GetShiftKey())

    if shift and ks == "f":
        view_shift_f()
    elif shift and ks == "b":
        view_shift_b()
    elif ks == "u":
        view_u()
    elif ks == "a":
        view_a()
    elif ks == "r":
        view_r()
    elif ks == "l":
        view_l()

v = GetActiveViewOrCreate("RenderView")
iren = v.GetInteractor()
if iren is not None:
    old = getattr(builtins, "_pv_all_hotkeys_obs", None)
    if old and old.get("iren") is iren:
        for oid in old["ids"]:
            try: iren.RemoveObserver(oid)
            except: pass
    ids = [iren.AddObserver("KeyPressEvent", on_key), iren.AddObserver("CharEvent", on_key)]
    builtins._pv_all_hotkeys_obs = {"iren": iren, "ids": ids, "cb": on_key}
    print("Installed: U, A, R, L, Shift+F, Shift+B")
else:
    print("No interactor found.")
