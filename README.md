# harmonic_demo

Steps to launch it:

```bash
cd ~/ws/src
vcs import < recepcionist_demo/thirdparty.repos
```

```bash
cd ~/ws
sudo rosdep init
rosdep update
colcon build --symlink-install
source install/setup.bash
```

Once colcon is done, we can launch our world without any problems:

```bash
ros2 launch harmonic_demo sim.launch.py
```