# magnetic-game-Aya
آية ساريج، فئة 3.
# توصيف:
برنامج بلغة بايثون يعمل على بناء لعبة logic_magnets ومحاولة محاكاتها ( لا زال قيد التطوير جتى يتضمن خوارزميات بحث متقدمة تحل المسألة تلقائيا)
يمكن للمستخدم البدء بلعب اللعبة واختيار المرحلة التي يريد أن يلعبها وأن يلعبها متجاوبا مع الconsole حاليا، اذ يتم رسم الرقعة وأخذ الأوامر من المستخدم لتحريك المغناطيسات حتى الوصول للفوز على الشكل التالي:
Enter the level number you want to play: 2
Starting Level with board size 5
Grid game state:
    0  1  2  3  4
 +---------------+
0|  .  .  T  .  . |
1|  .  .  I  .  . |
2|  T  I  T  I  T |
3|  .  .  I  .  . |
4|  R  .  T  .  . |
 +---------------+
Enter the coordinates of the piece you want to move (x y): 4 0
Enter the new coordinates for the piece (new_x new_y): 2 2
Piece moved.
Grid game state:
    0  1  2  3  4
 +---------------+
0|  .  .  I  .  . |
1|  .  .  .  .  . |
2|  I  .  R  .  I |
3|  .  .  .  .  . |
4|  .  .  I  .  . |
 +---------------+
Congratulations! You've completed the level!
حيث يمثل:
الهدف target بالحرف T
الحديد الجاذب (attractive) بالرمز A
المغناطيس النافر (repulsive) بالرمز R
القطع الحديدية بالرمز I


# ملاحظة:
لمن يحب أن يجرب اللعبة يمكنه أن يستخدم الرابط التالي: https://www.mathplayground.com/logic_magnets.html
