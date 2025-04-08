# [Prospectin'](https://plaidctf.com/challenge/7) (rev)

The challenge was reverse engineer two binaries. 

## Part 1 - Fool's Gulch

- Decompiling the binary yielded a program which reads a candidate flag and outputs whether the flag is correct.
- This is done through a lot of ifs (400 of them), each if increases the score by one (bumps it):
  ```
  if (local_3a == 0x32) {
    bump(&score);
  }
  if ((local_36 ^ local_3d) == 0xaa) {
    bump(&score);
  }
  if ((byte)(local_36 + local_27) == -0x70) {
    bump(&score);
  }
  ... 397 more
  ```
- Quite straightforward, we dumped it into Gemini 2.5 Pro with instructions to convert it to z3 conditions, this solved it directly.

## Part 2 - The Motherlode (upsolved)

- The second binary was similar, but had more ifs and considerably trickier conditions:
  ```
  if ((((byte)(local_59 + local_42 & local_3c) <
      (byte)((local_53 + local_43) - local_40)) &&
      ((local_4d - local_4c & local_4a) < 0x27)) &&
    ((byte)(local_4e + local_45 * local_5a) <
      (byte)((local_44 + local_43) * local_42))) {
    yeet(&scores);
  }
  if ((((byte)(local_5a * local_37 - local_31) < 200) &&
       (0x3c < (byte)((local_2d - local_33) + local_51))) &&
      ((0x4c < (byte)((local_2b + local_3b) - local_57) &&
        ((byte)(local_45 - (local_54 + local_2e)) <
         (byte)(local_4f * local_2e ^ local_52))))) {
    bump(&scores);
  }
  ...
  ```
- Now there were multiple possible ways to increase the score, not only bump, either +1, +2, +4, +8 or any combination of them.
- This was too much to enter into current llms, so we wrote a converter to convert the ifs into z3 conditions.
- Then we set the goal to maximize and let it run, this however never finished, even during the night
- We made multiple optimizations during that time, such as adding conditions for the known part of the flag (`PCTF{` and `}`) and assuming that the flag itself only contains hex values, as it did only contain hex values in part 1. This was not enough though.
- So we did not manage to solve this during the contest.

### Changes to make it work

Aftwerwards we had to make two changes to the code in order to have it find the flag:

- Use `Optimize::set_on_model` in order to print the current best model. This challenge apparently contains loops (a < b < c < a), which are not possible to prove for z3 as I understand it. Therefore it never finishes, despite finding the flag.
- Use [ULT and ULG](https://microsoft.github.io/z3guide/programming/Z3%20Python%20-%20Readonly/Introduction#machine-arithmetic) instead of < >, as apparently in z3 BitVec's are not signed, but some of the operators have two variants, a signed and unsigned version. This meant that our initial program was wrong and could not have found the flag anyways.

This finds the flag in 43 seconds on my machine, but does not terminate.

### Further learnings:

- The function opt.add_soft() allows you to assign weights to specific conditions. I applied the score’s weight to every if condition, which sped up the process by about 10 seconds—roughly a 20% improvement.
- The expression If(cond, w, 0) is equivalent to cond * w, performance-wise, as expected.
- Using simplify didn’t make a significant difference in the end; in fact, it sometimes slowed things down. Without some of the simplify calls, it finds a solution in 24 seconds, but without using all of them, it takes 57 seconds. This timing might also depend on the seed.
- Genetic algorithms would likely have worked very well for this task. I noticed that the code was quite short, and it would probably run in only about 3 seconds.
- Limiting the search space and making the simple assumption that the flag consists only of hexadecimal characters was essential.
- Without using a maximize function (and relying solely on the condition objective > 0x5f2), the flag is not found - even when using Optimize instead of Solver.
- The Solver() class doesn’t find a solution either. It appears that Optimize() must be used instead because Solver() lacks a set_on_model function and does not maintain a notion of the best model so far, making it unsuitable for this task
