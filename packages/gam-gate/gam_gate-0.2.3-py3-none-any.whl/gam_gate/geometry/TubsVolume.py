import gam_gate as gam
import gam_g4 as g4


class TubsVolume(gam.VolumeBase):
    """
    http://geant4-userdoc.web.cern.ch/geant4-userdoc/UsersGuides/ForApplicationDeveloper/html/Detector/Geometry/geomSolids.html
    pRMin SetInnerRadius
    pRMax SetOuterRadius
    pDz  SetZHalfLength
    pSPhi SetStartPhiAngle
    pDPhi SetDeltaPhiAngle
    """

    type_name = 'Tubs'

    @staticmethod
    def set_default_user_info(user_info):
        gam.VolumeBase.set_default_user_info(user_info)
        # default values
        u = user_info
        mm = gam.g4_units('mm')
        deg = gam.g4_units('deg')
        u.Rmin = 30 * mm
        u.Rmax = 40 * mm
        u.Dz = 40 * mm
        u.SPhi = 0 * deg
        u.DPhi = 360 * deg

    def build_solid(self):
        u = self.user_info
        return g4.G4Tubs(u.name, u.Rmin, u.Rmax, u.Dz, u.SPhi, u.DPhi)
