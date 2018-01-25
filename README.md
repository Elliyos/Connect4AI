# Connect4AI

Interactive graph showing thinking times across opponents:
https://plot.ly/~elliyos/0/minimax-vs-human-minimax-vs-random-minimax-vs-minimax/

Connect4AI system is designed using a heuristic that assesses performance 
based on how close each player is to a win. It tracks how many pairs of 
two and three it has, and it also tracks how many pairs of both the opponent 
has. In an attempt to place a higher importance on the opponent’s pairs, 
they are weighted higher than the pairs of the player. For example, one 
pair of three is worth three points for the player; for the opponent, a 
pair of three is actually worth four points. The opponent’s points are 
subtracted from the player’s points to give a heuristic value. It runs 
over five times as fast, on average, using the alpha-beta pruning. The AI 
is a formidable opponent at 3 ply, but at 5 ply is becomes a nightmare. 
Any higher is even worse, but the thinking time is far too long to try 
that much.
