# AgentsInfo - Observation, Action, Reward

## Vector Observations:
* Vehicle velocity (Vector3)
* Vehicle relative position to success area (Vector3)
* Vehicle Y-axis<sup>1</sup> rotation angle (float)

## Visual Observations:
* Up to 3 cameras image output
* More info about [Image output type](ML-ImageSynthesis.md) and [How to configure camera](Setup-Configuration-Files.md#environment-config)

## Actions:
* +30, 0, -30 degree of streeing angle 
* +1, 0, -0.3 scale of throttle power.
Total combination of 9 discrete actions

## Rewards:
* Time penalty: -1 / timestep
* Drive on the grass: -300
* Collide with barriers: -300
* Distance<sup>2</sup> between agent and success area:<br> 
  ```max((last_timestep_distance - current_timestep_distance), 0) * 300```
* Velocity reward: +1/ m/s 
* Succeed: +500
* More info about [Customize reward values](Setup-Configuration-Files.md#environment-config)

## Episode End Condiition:
* Time step > 1500 (30s environment time)
* Collide with barriers
* Drive on the grass
* Succeed

## Definition of Succeed:
* All 4 wheels in the success area, and 
```Vector3.Dot(VehicleForwardUnitVector, SuccessAreaForwardUnitVector) < 0.5```



<sup>1</sup> Y-axis is the vertical axis in Unity<br>
<sup>2</sup> Unity uses SI units<br>
