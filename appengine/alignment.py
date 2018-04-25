import numpy as np

class Alignment:
	def __init__(self, type='global'):
		self.type = 'global'

	def traceback(self, grid, trace, seq1, seq2):
		opt_align = []
		align1 = ''
		align2 = ''
		i, j = np.unravel_index(grid.argmax(), grid.shape)
		
		while i > 0 and j > 0:
			next_step = str(trace[i][j])
			if 'up' in next_step:
				align1 = seq1[i-1] + align1
				align2 = '_' + align2
				i -= 1
			elif 'left' in next_step:
				align1 = '_' + align1
				align2 = seq2[j-1] + align2
				j -= 1
			elif 'diag' in next_step:
				align1 = seq1[i-1] + align1
				align2 = seq2[j-1] + align2
				i -= 1
				j -= 1
		
		opt_align.append(align1)
		opt_align.append(align2)
		
		return opt_align
	def alignment(self, sequence_1, sequence_2, alignment_type='global', match_score=1, mismatch_score=-1, linear_gap=-3):
		if alignment_type not in ('global', 'local'):
			return False
		seq_1_len = len(sequence_1) + 1
		seq_2_len = len(sequence_2) + 1
		
		grid = np.zeros((seq_1_len, seq_2_len))
		trace = np.zeros((seq_1_len, seq_2_len)).tolist()
		
		# init matrix with edges gap penelty
		if alignment_type == 'global':
			for i in range(seq_1_len):
				grid[i][0] = linear_gap * i
			for j in range(seq_2_len):
				grid[0][j] = linear_gap * j
		elif alignment_type == 'local':
			for i in range(seq_1_len):
				grid[i][0] = 0
			for j in range(seq_2_len):
				grid[0][j] = 0
				
		print grid
		

		for i in range(1, seq_1_len):
			for j in range(1, seq_2_len):

				## does diag_match?
				if sequence_1[i-1] == sequence_2[j-1]:
					match_boost = match_score
				else:
					match_boost = mismatch_score

				if alignment_type == 'global':
					up   = grid[i-1][j] + linear_gap
					left = grid[i][j-1] + linear_gap
					diag = grid[i-1][j-1] + match_boost
					grid[i][j] = max(up, left, diag)
					trace_pointer = ''
					if up == grid[i][j]:
						trace_pointer += 'up'
					if left == grid[i][j]:
						trace_pointer += 'left'
					if diag == grid[i][j]:
						trace_pointer += 'diag'
					trace[i][j] = str(trace_pointer)
				elif alignment_type == 'local':
					diag = grid[i-1][j-1] + match_boost
					grid[i][j] = max(diag, 0)
					if diag > 0:
						trace[i][j] = 'diag'
		alignment = self.traceback(grid, trace, sequence_1, sequence_2)
		# print alignment
		return grid, trace, alignment, int(grid.max())