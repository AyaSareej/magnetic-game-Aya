

# Magnetic Game - Aya

آية ساريج، فئة 3.

## توصيف

برنامج بلغة بايثون يعمل على بناء لعبة **Logic Magnets** ومحاولة محاكاتها (لا زال قيد التطوير حتى يتضمن خوارزميات بحث متقدمة تحل المسألة تلقائياً). يمكن للمستخدم البدء بلعب اللعبة واختيار المرحلة التي يريد أن يلعبها، واللعب متجاوباً مع الـ console حالياً. يتم رسم الرقعة وأخذ الأوامر من المستخدم لتحريك المغناطيسات حتى الوصول للفوز.

### كيفية اللعب

1. أدخل رقم المرحلة التي تريد اللعب بها:
Enter the level number you want to play: 2

Copy

2. تبدأ المرحلة مع حجم الرقعة:
Starting Level with board size 5

Copy

3. حالة اللعبة على الرقعة:
Grid game state:
0 1 2 3 4
+---------------+
0| . . T . . |
1| . . I . . |
2| T I T I T |
3| . . I . . |
4| R . T . . |
+---------------+

Copy

4. أدخل إحداثيات القطعة التي تريد تحريكها (x y):
Enter the coordinates of the piece you want to move (x y): 4 0

Copy

5. أدخل الإحداثيات الجديدة للقطعة (new_x new_y):
Enter the new coordinates for the piece (new_x new_y): 2 2

Copy

6. ستظهر لك الرسالة التالية عند نجاح التحريك:
Piece moved.

Copy

7. حالة اللعبة بعد التحريك:
Grid game state:
0 1 2 3 4
+---------------+
0| . . I . . |
1| . . . . . |
2| I . R . I |
3| . . . . . |
4| . . I . . |
+---------------+

Copy

8. في النهاية، ستظهر لك رسالة التهنئة:
Congratulations! You've completed the level!

Copy

### الرموز المستخدمة

- **T**: الهدف (target)
- **A**: الحديد الجاذب (attractive)
- **R**: المغناطيس النافر (repulsive)
- **I**: القطع الحديدية

## ملاحظة

لمن يحب أن يجرب اللعبة، يمكنه استخدام الرابط التالي: [Logic Magnets](https://www.mathplayground.com/logic_magnets.html)
يمكنك نسخ هذا التنسيق ولصقه في ملف README.md الخاص بمشروعك على GitHub. تأكد من استخدام علامات Markdown بشكل صحيح لتنسيق النص.

