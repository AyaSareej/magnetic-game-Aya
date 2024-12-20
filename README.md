# Magnetic Game - Aya

آية ساريج، فئة 3.

## توصيف

برنامج بلغة بايثون يعمل على بناء لعبة **Logic Magnets** ومحاولة محاكاتها (لا زال قيد التطوير حتى يتضمن خوارزميات بحث متقدمة تحل المسألة تلقائياً). يمكن للمستخدم البدء بلعب اللعبة واختيار المرحلة التي يريد أن يلعبها، واللعب متجاوباً مع الـ console حالياً. يتم رسم الرقعة وأخذ الأوامر من المستخدم لتحريك المغناطيسات حتى الوصول للفوز. يتم تمثيل الحالة كرقعة n × n تحتوي على كامل مواضع القطع المختلفة ممثلة بأحرف كبيرة.

## كيفية اللعب

1. أدخل رقم المرحلة التي تريد اللعب بها:
Enter the level number you want to play: 2
Starting Level with board size 5

4. أدخل إحداثيات القطعة التي تريد تحريكها (x y):
Enter the coordinates of the piece you want to move (x y): 4 0


5. أدخل الإحداثيات الجديدة للقطعة (new_x new_y):
Enter the new coordinates for the piece (new_x new_y): 2 2

6. ستظهر لك الرسالة التالية عند نجاح التحريك:
Piece moved.


Grid game state:

  0   1   2   3   4
  
 +-------------------+
 
0 | .   .   I   .   . |

 
1 | .   .   .   .   . |

 
2 | I   .   R   .   I |

 
3 | .   .   .   .   . |


4 | .   .   I   .   . |

 +-------------------+
 

8. في النهاية، ستظهر لك رسالة التهنئة:
Congratulations! You've completed the level!


## الرموز المستخدمة

- **T**: الهدف (target)
- **A**: الحديد الجاذب (attractive)
- **R**: المغناطيس النافر (repulsive)
- **I**: القطع الحديدية

## فضاء الحالات (State Space)

### تمثيل الحالة
تُعتبر الحالة تمثيلًا لرقعة n × n، حيث تمثل كل خانة في الرقعة إما خانة فارغة، أو تحتوي على قطعة حديدية (الرمادية)، أو قطعة مغناطيسية (البنفسجية للحركة الجاذبة والحمراء للحركة النافرة). كما تحتوي الرقعة على خانات الهدف التي يجب تغطيتها لتحقيق الفوز.

### محتويات الحالة
تتضمن معلومات عن:
- **موقع كل قطعة:** يتم تخزين المواقع لكل قطعة حديدية أو مغناطيسية في الشبكة باستخدام إحداثيات `[x, y]`.
- **حالة كل خانة:** يتم تحديد حالة كل خانة كالتالي:
- **فارغة:** لا تحتوي على أي قطعة.
- **مملوءة:** تحتوي على قطعة مغناطيسية أو حديدية.
- **هدف:** تحتوي على خانة هدف (تُعرف بالدوائر البيضاء).

## الحالة الابتدائية (Initial State)

تُحدد الحالة الابتدائية عند بدء اللعبة، حيث تشمل:
- **مواقع القطع:** يتم تحديد مواقع القطع المغناطيسية (الجاذبة والنافرة) والحديدية في الشبكة.
- **خانات الهدف:** تُحدد مواقع خانات الهدف التي يجب على اللاعب تغطيتها. يتم استخدام قائمة لتخزين هذه المواقع، مما يسهل التحقق من تحقيق الفوز في نهاية اللعبة.

## العمليات (Actions)

### تحريك القطع المغناطيسية
- **القطعة البنفسجية (الجاذبة):** 
- يمكن تحريكها إلى أي خانة فارغة. 
- عند تحريكها، تتجاذب القطع الحديدية المجاورة لها في السطر أو العمود، مما يؤدي إلى تحريك القطع الحديدية في الاتجاه المعاكس للقطعة الجاذبة.

- **القطعة الحمراء (النافرة):** 
- يمكن تحريكها أيضًا إلى أي خانة فارغة.
- عند تحريكها، تتنافر القطع الحديدية المجاورة لها، مما يؤدي إلى دفع القطع الحديدية بعيدًا عنها.

### القيود على التحريك
- **القطع الحديدية (الرمادية):** لا يمكن تحريكها مباشرة. تتحرك فقط استجابةً لتأثير القطع المغناطيسية (التنافر أو التجاذب). 
- **التحقق من الحدود:** يتم التحقق من أن الإحداثيات الجديدة تقع ضمن حدود الرقعة قبل تنفيذ أي حركة.

## الحالات النهائية (Goal States)

تعتبر الحالة النهائية قد تحققت عندما يتم تغطية جميع خانات الهدف (الخانات التي تحتوي على الدوائر البيضاء) بقطع حديدية أو مغناطيسية. يتم التحقق من ذلك من خلال مقارنة مواقع خانات الهدف مع الحالة الحالية للرقعة. إذا كانت جميع خانات الهدف مملوءة بقطع حديدية أو مغناطيسية، يتم إعلان فوز اللاعب.

## الهيكل العام للعبة

### الفئات الأساسية
- **Piece:** تمثل قطعة في اللعبة، تحتوي على نوع القطعة (جاذبة، نافرة، حديدية) وموقعها.
- **Board:** تمثل الرقعة، وتحتوي على طرق لإضافة قطع، عرض الحالة الحالية للرقعة، والتحقق من إمكانية الحركة.
- **Level:** تمثل مستوى اللعبة، تحتوي على إعدادات المستوى، وتبدأ اللعبة، وتدير حلقة اللعب.
- **Game:** تدير اللعبة بشكل عام، وتسمح للاعب باختيار المستوى الذي يريد اللعب فيه.

  ## أهم التوابع المستخدمة

### 1. `initialize_board(size)`
تقوم هذه الدالة بتهيئة الرقعة بحجم محدد، وتملأها بالخانات الفارغة.

### 2. `display_board(board)`
تقوم هذه الدالة بعرض حالة الرقعة الحالية بتنسيق منظم، مما يسهل على اللاعب رؤية مواقع القطع.

### 3. `move_piece(piece, new_x, new_y)`
تقوم هذه الدالة بتحريك القطعة إلى الإحداثيات الجديدة المحددة، مع التحقق من صحة الحركة وفقًا لقواعد اللعبة.

### 4. `check_win_condition(board, targets)`
تتحقق هذه الدالة مما إذا كانت جميع خانات الهدف قد تم تغطيتها بقطع حديدية أو مغناطيسية، وتعيد قيمة Boolean تحدد ما إذا كانت اللعبة قد انتهت بالفوز.

### 5. `get_valid_moves(piece, board)`
تقوم هذه الدالة بإرجاع قائمة بالإحداثيات الممكنة التي يمكن للقطعة التحرك إليها، بناءً على موقعها الحالي والقواعد المعمول بها.

### 6. `apply_magnet_effect(board)`
تقوم هذه الدالة بتطبيق تأثيرات المغناطيس على القطع الحديدية المجاورة عند تحريك قطعة مغناطيسية، سواء كانت جاذبة أو نافرة.

### 7. `load_level(level_number)`
تقوم هذه الدالة بتحميل إعدادات المستوى المحدد، بما في ذلك مواقع القطع وخانات الهدف.

### 8. `main()`
تدير هذه الدالة الحلقة الرئيسية للعبة، حيث تتفاعل مع اللاعب وتنسق بين جميع التوابع الأخرى.


### التفاعل مع اللاعب
يتم استخدام واجهة سطر الأوامر (console) للتفاعل مع اللاعب، حيث يُطلب منه إدخال إحداثيات القطع التي يريد تحريكها والإحداثيات الجديدة. يتم التحقق من صحة الإدخالات، وتُعرض رسائل توضح حالة اللعبة بعد كل حركة.

## ملاحظة

لمن يحب أن يجرب اللعبة، يمكنه استخدام الرابط التالي: [Logic Magnets](https://www.mathplayground.com/logic_magnets.html)

استمتع باللعبة!


