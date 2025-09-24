# Balls-of-steel-simulation<br>
Physics based simulation || run the final.py <br>
<br>
This project simulates a Mass object (ball) in a system where it experiences the following forces and actions:<br>
1. Gravity <br>
2. Friction <br>
3. Collision with wall <br>
4. masses can be grabbed and swing using mouse pointer (momentum) <br>
5. energy loss on bouncing. <br>
<br>
<h2>Concepts used:</h2>
1. How do we calculate collision between the floor and mass (ball)?
<br><br>

  <img width="1013" height="570" alt="concept" src="https://github.com/user-attachments/assets/73ee3bdc-f171-4310-b6dc-f2518ff1f4d7" /><br>
  <p>
     The centre of circle act as the primary point for the whole circle. The floor has a thickness of 't' then it is divided into half by the screen's boundary (shown by red line in below image. for example: if our floor thickness is 10px then the 5px is under the screen and 5px is above the screen. Since for a circle it's primary point is it's centre that's why we need to imagine the floor at centre of cirlce. Subtract the thickness of floor and radius from the overall HEIGHT of the screen we would get the pseudo floor at centre of the circle.
    <br><br>
    same concept has been used with side wall's collision too. 
    <br>
    <img width="1503" height="780" alt="concept3" src="https://github.com/user-attachments/assets/5d2b7334-a491-493f-9a3d-34d2e30030f7" />
    <br>
  </p>
<br>
2. How mass's (ball's) speed will decrease when it will be going up?
<br>
<img width="1612" height="706" alt="concept2" src="https://github.com/user-attachments/assets/1abed092-74bc-4bf4-ae43-c8eaf6ea1883" />
<br><br>

<h3>Thank you, feel free to repo if find useful.
<br>
  Created by: Aryan Mishra
</h3>



