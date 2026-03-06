from paraview.simple import *
import builtins

def fit_view(reset_fn, roll=None):
    v = GetActiveViewOrCreate("RenderView")
    v.Set(
        InteractionMode="Selection",
        CameraParallelProjection=1,
    )
    reset_fn(v)
    v.ResetCamera(False, 0.9)
    if roll is not None:
        v.AdjustRoll(roll)
    Render(v)

# Gaming-style mapping:
# W = Front, S = Back, A = Left, D = Right, Q = Top, E = Bottom
def view_w_front():
    fit_view(lambda v: v.ResetActiveCameraToNegativeZ())

def view_s_back():
    fit_view(lambda v: v.ResetActiveCameraToPositiveZ())

def view_a_left():
    fit_view(lambda v: v.ResetActiveCameraToPositiveX(), roll=-90.0)

def view_d_right():
    fit_view(lambda v: v.ResetActiveCameraToNegativeX(), roll=90.0)

def view_q_top():
    fit_view(lambda v: v.ResetActiveCameraToPositiveY())

def view_e_bottom():
    fit_view(lambda v: v.ResetActiveCameraToNegativeY())

def on_key(interactor, event):
    ks = (interactor.GetKeySym() or "").lower()

    if ks == "w":
        view_w_front()
    elif ks == "s":
        view_s_back()
    elif ks == "a":
        view_a_left()
    elif ks == "d":
        view_d_right()
    elif ks == "q":
        view_q_top()
    elif ks == "e":
        view_e_bottom()

v = GetActiveViewOrCreate("RenderView")
iren = v.GetInteractor()

if iren is None:
    print("No interactor found. Click inside Render View and run again.")
else:
    old = getattr(builtins, "_pv_wasdqe_obs", None)
    if old and old.get("iren") is iren:
        for oid in old["ids"]:
            try:
                iren.RemoveObserver(oid)
            except:
                pass

    ids = [
        iren.AddObserver("KeyPressEvent", on_key),
        iren.AddObserver("CharEvent", on_key),
    ]
    builtins._pv_wasdqe_obs = {"iren": iren, "ids": ids, "cb": on_key}
    print("Installed hotkeys: W=Front, S=Back, A=Left, D=Right, Q=Top, E=Bottom (auto-fit)")

