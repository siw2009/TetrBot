# This is a Tetr.io bot

여러분 여기에 뭘 적어야 할까요

자랑하기엔 인터페이스도 제대로 구축이 안됐는데..흠

시험 끝나고 시간 남는 사람이 적읍시다ㅇㅇ

![img](HTML.png)

세계 0위

&nbsp;

# 다음 섹션은 간략히 수학을 다룹니다

이 tetr.io 봇은 `라그랑주 보간법`과 `simpson’s rule`을 사용해 해법을 근사하며, `퍼펙트 클리어`와 `T spin`을 해낼 수 있는 가장 최적의 해를 `next`와 `hold`를 매개변수로 사용하여 구한다. 라그랑주 보간법은 다음과 같이 정의된다.

데이터의 개수가 $l$개 있다고 하면,

$$f \left( x \right) =\sum _{n=0}^{l} \, \left( y_{n} \prod _{k=0 \wedge k\neq n}^{l} \, \frac { \left( x-x_{k} \right) } {\left( x_{n}-x_{k} \right) } \right)$$

정말 간단하다. 이를 python에서 구현하는 것도 2중 for 문이면 가능한 것이다. *(비싸긴 하네)*

심슨 규칙은 다음과 같이 정의된다. 이 규칙은 어떤 함수의 미분꼴은 간단하지만 그냥 함숫값은 구하기 *~~개같을~~* 때 사용하는 공식이다. 즉, 미분꼴의 적분값을 근사하여 실제 함수의 함숫값을 근사하는 것이다. $ln$ 근사에 사용하기에 딱 좋아보이지 않는가?
$$\int ^{a} _{b} f \left( x \right) \, dx \approx \frac {b-a} {6} \left[ f \left( a \right) + 4f\left( \frac {a+b} {2} \right) + f \left( b \right) \right]$$
이를 이진탐색과 결합하면 자연상수 $e$의 값을 근사하는 것도 가능하며, `math` 라이브러리의 값과 비교했을 때, 꽤 정확한 결과값을 내놓는다.

&nbsp;

# 자세한 내용은 [여기](https://en.wikipedia.org/wiki/Simpson%27s_rule)와 [여기](https://en.wikipedia.org/wiki/Lagrange_polynomial)를 참고하자.
# 이 두 방식을 구현한 [R&E 리포의 코드](https://github.com/siw2009/Sabermetrics_research/blob/656af993cac139a0c9616fa83191dc0c27dfcf00/logarithm.py)를 읽어보는 것도 좋다.