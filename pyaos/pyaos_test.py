import pyaos.lfr as LFR
import cv2
import os
import unittest
import sys
import glm
import numpy as np
import numpy.testing
from pathlib import Path


class TestAOSRenderTwice(unittest.TestCase):

    _window = None
    _aos1 = None
    _aos2 = None
    _fovDegrees = 50

    def setUp(self):
        print('---SETUP---')
        if self._window is None: 
            self._window = LFR.PyGlfwWindow(512,512,'AOS') # make sure there is an OpenGL context
        #print( 'initializing AOS ... ' )
        self._aos1 = LFR.PyAOS(512,512,self._fovDegrees)
        self._aos2 = LFR.PyAOS(512,512,self._fovDegrees)
        # loading DEM
        self._aos1.loadDEM("../data/zero_plane.obj")
        self._aos2.loadDEM("../data/zero_plane.obj")

    def tearDown(self):
        print('---TEARDOWN---')
        del self._aos1
        del self._aos2
        del self._window
        self._window = None

    def test_render_twice(self):
        self.color_image(self._aos1)
        self.render_single_image(self._aos1)
        self.render_single_image(self._aos2)
        self.matrices_tests()

    def render_single_image(self, _aos):

        img = np.ones(shape=(512,512,1), dtype = np.float32)
        pose = np.eye(4)

        
        # adding a view
        self.assertTrue(_aos.getSize()==0)
        _aos.addView( img, pose, "01" )
        self.assertTrue(_aos.getSize()==1)
        #print( f"size of aos: {_aos.getSize()}" )

        ztransl = -100
        _aos.setDEMTransform( [0,0,ztransl] )
        rimg = _aos.render(pose, self._fovDegrees)

        # check that the rendered image is like the initial one
        #print( img )
        #print( rimg )
        self.assertTrue(np.allclose(img[:,:,0],rimg[:,:,0],atol=1.e-4))

        # adding a second view:
        img2 = np.ones(shape=(512,512,1), dtype = np.float32) * 2.0

        self.assertTrue(_aos.getSize()==1)
        _aos.addView( img2, pose, "02" )
        self.assertTrue(_aos.getSize()==2)

        rimg2 = _aos.render(pose, self._fovDegrees)
        rimg2 = rimg2[:,:,0] / rimg2[:,:,3]

        # check that the rendered image an average of the first and the second one! (1 + 2)/2 = 1.5
        self.assertTrue(np.allclose(rimg2, np.ones(shape=(512,512), dtype = np.float32) * 1.5))
        self.assertTrue(np.allclose(img[:,:,0],rimg[:,:,0])) # check that rimg has not changed!


        # replacing the second view with a new one
        img3 = np.ones(shape=(512,512), dtype = np.float32) * 3.0

        self.assertTrue(_aos.getSize()==2)
        _aos.replaceView( 1, img3, pose, "03" )
        self.assertTrue(_aos.getSize()==2)

        rimg = _aos.render(pose, self._fovDegrees)
        rimg = rimg[:,:,0] / rimg[:,:,3]

        # check that the rendered image is an average of the first and the thrid one! (1 + 3)/2 = 2.0
        self.assertTrue(np.allclose(rimg, np.ones(shape=(512,512), dtype = np.float32) * 2.0))

        # render only the third one
        rimg = _aos.render(pose, self._fovDegrees, [1])
        rimg = rimg[:,:,0] / rimg[:,:,3]

        # check that the rendered image is like the third image
        self.assertTrue(np.allclose(rimg, np.ones(shape=(512,512), dtype = np.float32) * 3.0))

        #cv2.imshow("Rendering",rimg)
        #cv2.waitKey(0)

        # get XYZ coordinates from plane.obj (z coordinate should be -100 everywhere)
        xyz = _aos.getXYZ()
        self.assertTrue(np.isclose(xyz[:,:,2],ztransl).all())

        # translate the DEM up 
        ztransl = -30
        _aos.setDEMTransform( [0,0,ztransl] )
        _aos.render(pose, self._fovDegrees, [1])
        xyz = _aos.getXYZ()
        print(xyz)
        self.assertTrue(np.isclose(xyz[:,:,2],ztransl).all())

        # translate the DEM down 
        ztransl = -120
        _aos.setDEMTransform( [0,0,ztransl] )
        _aos.render(pose, self._fovDegrees, [1])
        xyz = _aos.getXYZ()
        print(xyz)
        #print(xyz[:,:,2])
        self.assertTrue(np.isclose(xyz[:,:,2],ztransl).all())

        _aos.removeView(0)
        self.assertTrue(_aos.getSize()==1)
        _aos.removeView(0)
        self.assertTrue(_aos.getSize()==0)

    def test_clear_view(self):
        img = np.ones(shape=(512,512,1), dtype = np.float32)
        pose = np.eye(4)
        _aos = self._aos1

        # adding 1 view
        self.assertTrue(_aos.getSize()==0)
        _aos.addView( img, pose, "01" )
        self.assertTrue(_aos.getSize()==1)

        _aos.clearViews()
        self.assertTrue(_aos.getSize()==0)

        # adding N views
        for n in range(10):
            self.assertTrue(_aos.getSize()==n)
            _aos.addView( img, pose, str(n) )
            self.assertTrue(_aos.getSize()==(n+1))
        
        _aos.clearViews()
        self.assertTrue(_aos.getSize()==0)


    def color_image(self,_aos):
        #_aos = self._aos1
        
        # color image with three channels
        img = np.ones(shape=(512,512,3), dtype = np.float32)
        img[:,:,0] = 0.1
        img[:,:,1] = 1.0
        img[:,:,2] = 3.0
        pose = np.eye(4)

        
        # adding a view
        self.assertTrue(_aos.getSize()==0)
        _aos.addView( img, pose, "c01" )
        self.assertTrue(_aos.getSize()==1)

        ztransl = -100
        _aos.setDEMTransform( [0,0,ztransl] )
        rimg = _aos.render(pose, self._fovDegrees)

        # check that the rendered image is like the initial one
        #print("python image: ")
        #print( img.shape )
        #print("LFR image: ")
        #print( rimg.shape )
        self.assertTrue(np.allclose(img[:,:,:3],rimg[:,:,:3],atol=1.e-4))

        # adding a second color image:
        # color image with three channels
        img2 = np.ones(shape=(512,512,3), dtype = np.float32)
        img2[:,:,0] = 0.2
        img2[:,:,1] = 0.75
        img2[:,:,2] = 3.0

        self.assertTrue(_aos.getSize()==1)
        _aos.addView( img2, pose, "c02" )
        self.assertTrue(_aos.getSize()==2)

        rimg2 = _aos.render(pose, self._fovDegrees)
        rimg2 = np.divide( rimg2[:,:,:3], np.stack((rimg2[:,:,3],rimg2[:,:,3],rimg2[:,:,3]),axis=-1) )

        self.assertTrue(np.allclose((img+img2)/2,rimg2[:,:,:],atol=1.e-4)) # check that rimg has not changed!

        _aos.clearViews()
        self.assertTrue(_aos.getSize()==0)

    def matrices_tests(self):
        aos = self._aos1
        
        # color image with three channels
        img = np.ones(shape=(512,512,3), dtype = np.float32)
        img[:,:,0] = 0.1
        img[:,:,1] = 1.0
        img[:,:,2] = 3.0
        
        #pose: mat4x4((0.995812, 0.005638, 0.091253, 0.000000), (-0.011608, 0.997817, 0.065017, 0.000000), (-0.090688, -0.065804, 0.993703, 0.000000), (0.052526, -0.020116, -0.174643, 1.000000)) name: B01_PICT0267.JPG size: 1024x1024x3
        pose = glm.transpose(glm.mat4(0.995812, 0.005638, 0.091253, 0.000000, -0.011608, 0.997817, 0.065017, 0.000000, -0.090688, -0.065804, 0.993703, 0.000000, 0.052526, -0.020116, -0.174643, 1.000000))
        #print(pose)
        
        # adding a view
        self.assertTrue(aos.getSize()==0)
        aos.addView( img, pose, "pose_test_01" )
        self.assertTrue(aos.getSize()==1)
        aos.addView( img, glm.mat4(2), "pose_test_02" )
        self.assertTrue(aos.getSize()==2)
        aos.addView( img, glm.mat4(3), "pose_test_03" )
        self.assertTrue(aos.getSize()==3)

        # retrieving pose again from LFR
        rpose = aos.getPose(0)
        #print(rpose)
        self.assertTrue(np.allclose(pose,rpose,atol=1.e-5)) # check the pose does not change!

        # set and get again
        aos.setPose(0,np.asarray(pose))
        r2pose = aos.getPose(0)
        #print(rpose)
        self.assertTrue(np.allclose(pose,r2pose,atol=1.e-5)) # check the pose does not change!
        #print('here?')

        # retrieve position and forward and up vectors and check if they are correct!
        ivp = glm.inverse(glm.transpose(glm.mat4(*aos.getPose(0).transpose().flatten())))
        pos = glm.vec3(ivp[3])
        up = glm.vec3(ivp[1])
        forward = glm.vec3(ivp[2])
        #print(pos)
        self.assertTrue(np.allclose(pos,[-0.036,0.032,0.177],atol=1.e-3)) # check pos, front and up!
        self.assertTrue(np.allclose(up,[0.006,0.998,-0.066],atol=1.e-3)) # check pos, front and up!
        self.assertTrue(np.allclose(forward,[0.091,0.065,0.994],atol=1.e-3)) # check pos, front and up!

        lA = glm.lookAt(pos, pos+forward, up)
        print(lA)
        
        # numpy interatcion
        npose = np.array(rpose)
        rnpose = glm.mat4(*npose.transpose().flatten())
        self.assertTrue(np.allclose(pose,rnpose,atol=1.e-5)) # check the pose does not change!

        nnpose = glm.mat4(*np.array(npose).transpose().flatten())
        self.assertTrue(np.allclose(pose,nnpose,atol=1.e-5)) # check the pose does not change!


        self.assertFalse(np.allclose(glm.mat4(1),glm.mat4(2),atol=1.e-5)) # check the pose does not change!


class TestAOSInit(unittest.TestCase):
    """ Test different scenarios for initialization

    """

    # standard initialization
    def test_init(self):
        window = LFR.PyGlfwWindow(512,512,'AOS') # make sure there is an OpenGL context
        #print( 'initializing AOS ... ' )
        aos = LFR.PyAOS(512,512,50,10)
        #print( 'aos created!' )

        del aos
        del window

    # initialization twice
    def test_init_two(self):
        window = LFR.PyGlfwWindow(512,512,'AOS') # make sure there is an OpenGL context
        #print( 'initializing AOS ... ' )
        aos1 = LFR.PyAOS(512,512,50,10)
        #print( 'aos created!' )

        aos2 = LFR.PyAOS(512,512,55)

        del aos1
        del aos2
        del window
    
    # initialization twice
    def test_init_twice(self):
        window = LFR.PyGlfwWindow(512,512,'AOS') # make sure there is an OpenGL context
        #print( 'initializing AOS ... ' )
        aos1 = LFR.PyAOS(512,512,50,10)
        del aos1
        del window
        #print( 'aos created!' )

        window = LFR.PyGlfwWindow(512,512,'AOS') # make sure there is an OpenGL context
        aos2 = LFR.PyAOS(512,512,55)
        del aos2
        del window

        
    def test_nocontext(self):
        # do it without valid opengl context

        errorRaised = False
        try:
            aos = LFR.PyAOS(512,512,50,10)
        except RuntimeError as err:
            print("Expected Runtime error: ",  err)
            errorRaised = True

        self.assertTrue(errorRaised)


# this test is not needed anymore!
"""    def test_shaderloading(self):
        # wrong working directory, so shaders cannot be loaded!

        olddir = os. getcwd()
        os.chdir('..')

        window = LFR.PyGlfwWindow(512,512,'AOS') # make sure there is an OpenGL context


        errorRaised = False
        try:
            aos = LFR.PyAOS(512,512,50,10)
        except RuntimeError as err:
            print("Runtime error: ",  err)
            errorRaised = True

        self.assertTrue(errorRaised)

        os.chdir(olddir)
"""



if __name__ == '__main__':

    file = Path(__file__).resolve()
    parent, root = file.parent, file.parents[1]

    #wd = os.getcwd()
    #os.chdir(parent) # change to AOS working dir for startup (this is required so that the program finds dlls and the shader)
    

    unittest.main()

    #os.chdir(wd) # change back to previous working directory