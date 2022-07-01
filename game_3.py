import pygame
import os
import time


pygame.init()
pygame.font.init()
pygame.mixer.init()

window = pygame.display.set_mode((900,500))
pygame.display.set_caption("Anya")
clock = pygame.time.Clock()

class word_guess:
	def __init__(self,length=0,columns_selected=[],transpose_columns_selected=[]):
		
		self.matrix = [['A','B','C','D','E','F'],
			['G','H','I','J','K','L'],
			['M','N','O','P','Q','R'],
			['S','T','U','V','W','X'],
			['Y','Z']]

		
		self.transposed_matrix = [['A','G','M','S','Y'],
				['B','H','N','T','Z'],
				['C','I','O','U'],
				['D','J','P','V'],
				['E','K','Q','W'],
				['F','L','R','X']]
		
		self.name_length = length
		self.columns_selected = columns_selected
		self.transpose_columns_selected = transpose_columns_selected
		self.calculated_name = self.calc_name()
	
	def calc_name(self):
		word_index = 0
		final = ''
		for _ in range(int(self.name_length)):
			final += self.matrix[int(self.transpose_columns_selected[word_index])-1][int(self.columns_selected[word_index])-1]
			word_index += 1
		return final

class Game:
	def __init__(self):

		self.guesser = word_guess()

		self.alpha = 0
		self.alpha_change = 1
		
		self.bg_done = False
		self.anya_done = False
		
		self.background = pygame.image.load_extended("bg.jpg").convert_alpha()
		self.anya_sprites = [pygame.transform.scale(pygame.image.load_extended("sprites\\no_bg\\"+img).convert_alpha(),(400,300)) for img in os.listdir("sprites\\no_bg")]

		self.button_pos = ''

		self.num_x = 229
		self.num_y = 452
		self.num_c = 0

		self.load_base()
		self.main()

	def bg_fade(self):

		if self.alpha == 255:
			self.bg_done = True
			self.alpha = 0
			self.alpha_change = 1

		self.alpha += self.alpha_change
		
		if not 0 <= self.alpha <= 255:
			self.alpha_change *= -1

		self.alpha = max(0,min(self.alpha,255))

		window.fill(0)


		alpha_image = self.background.copy()
		alpha_image.set_alpha(self.alpha)
		window.blit(alpha_image,(0,0))

		pygame.display.update()


	def fade_anya(self,img):

		if self.alpha == 255 or self.anya_done:
			self.anya_done = True
			self.alpha = 0
			self.alpha_change = 1
		else:

			self.alpha += self.alpha_change+2
			
			if not 0 <= self.alpha <= 255:
				self.alpha_change *= -1

			self.alpha = max(0,min(self.alpha,255))


			alpha_image = img.copy()
			alpha_image.set_alpha(self.alpha)
			window.blit(alpha_image,(328,132))

			pygame.display.flip()

	def draw_diag_rect(self):

		font_style = pygame.font.Font(None, 30)
		color = (0,0,0)
		x = 9
		y = 375
		c = 0

		pygame.draw.rect(window,color,pygame.Rect(x, y, 880, 120))
		pygame.draw.rect(window,(255,255,255),pygame.Rect(x, y, 880, 120), 2)
		self.button_pos = pygame.Rect(830,445,50,50)
		pygame.draw.rect(window, (255,255,255), self.button_pos)
		button = font_style.render("OK", True, (255,0,0))
		window.blit(button,(842,462))
		pygame.display.update()

	def draw_matrix(self):
		c = 0
		n = 1

		x = 3
		y = 49
		font_style = pygame.font.Font(None, 50)
		pygame.draw.rect(window,(0,0,0), pygame.Rect(0,0,300,300))
		pygame.draw.rect(window,(255,255,255),pygame.Rect(0,0,300,300), 2)
		
		for i in ["1.","2.","3.","4.","5.","6."]:
			col = font_style.render(i, True, (255,255,255))
			window.blit(col,(x+c,13))
			c+=50
			pygame.display.update()
		c = 0

		for i in self.guesser.matrix:
			for k in i:
				columns = font_style.render(k, True, (255,0,0))
				if n != len(i):
					if c == 0:
						window.blit(columns,(x,y))
						pygame.display.update()
						c+=50
						n+=1
					elif c!=0:
						window.blit(columns,(x+c,y))
						c+=50
						n+=1
				elif n == len(i):
					window.blit(columns,(x+c,y))
					y+=30
					n = 1
					c = 0

	def draw_matrix_transpose(self,cols):

		c = 0
		n = 1

		x = 3
		y = 49

		font_style = pygame.font.Font(None, 50)
		pygame.draw.rect(window,(0,0,0), pygame.Rect(0,0,300,300))
		pygame.draw.rect(window,(255,255,255), pygame.Rect(0,0,300,300), 2)
		pygame.display.update()	

		for i in ["1.", "2.", "3.","4.","5.","6."]:
			col = font_style.render(i, True, (255,255,255))
			window.blit(col,(x+c,13))
			c+=50
			pygame.display.update()
		c = 0

		for col in cols:
			for k in self.guesser.transposed_matrix[int(col)-1]:
				col_ = font_style.render(k, True, (255,0,0))
				if n!= len(self.guesser.transposed_matrix[int(col)-1]):
					if c == 0:
						window.blit(col_,(x,y))
						pygame.display.update()
						c+=50
						n+=1
					elif c!=0:
						window.blit(col_,(x+c,y))
						pygame.display.update()
						c+=50
						n+=1

				elif n == len(self.guesser.transposed_matrix[int(col)-1]):
					window.blit(col_,(x+c,y))
					pygame.display.update()
					y+=30
					n = 1
					c = 0

	def reload_(self):
		window.fill(0)
		window.blit(self.background,(0,0))

	def reload_anya(self,img):
		window.blit(img,(328,132))

	def play_diags(self):
		pygame.mixer.music.load('welcome_to_anya_house.mp3')
		pygame.mixer.music.play(0)

	def display_diag(self,text,mode=0):

		x = 12
		y = 375

		c = 0
		n = 1

		sleep_count = 0.05

		font_style = pygame.font.Font(None, 40)

		if mode == 1:
			sleep_count = 0
		
		self.draw_diag_rect()
		for i in text:
			diag = font_style.render(i, True, (255,255,255))
			window.blit(diag,(x+c,y))
			pygame.display.update()
			time.sleep(sleep_count)
			c+=18


	def display_input_prompt(self,text,num=None,mode=0):

		color = (0,255,0)

		font_style = pygame.font.Font(None, 40)
		prompt = font_style.render(text, True, (0,255,0))
		window.blit(prompt,(16,444))
		pygame.display.update()

		if num:
			if mode == 2:
				color = (0,0,0)
				if self.num_c != 0:
					self.num_c -= 14
					pygame.draw.rect(window,color,pygame.Rect(self.num_x+self.num_c, self.num_y, 16, 40))
					pygame.display.update()

			elif mode == 3:
				color = (0,0,0)
				self.num_c = 0
				self.num_x = 229

				pygame.draw.rect(window,color,pygame.Rect(229, self.num_y, 16, 40))
				pygame.display.update()
			else:
				window.blit(font_style.render(num, True, color),(self.num_x+self.num_c,self.num_y))
				pygame.display.update()
				if mode == 1:
					pass
				else:
					self.num_c+=14

	def check_button_click(self,pos):
		if self.button_pos.collidepoint(pos):
			return True
		else:
			return False


	def load_base(self):
		bg_music = pygame.mixer.Sound('bg_music.mp3')
		channel_0 = pygame.mixer.Channel(0)
		channel_0.set_volume(0.2)
		channel_0.set_endevent(pygame.USEREVENT+1)
		channel_0.play(bg_music)
		
		while True:
			clock.tick(60)
			if not self.bg_done:
				self.bg_fade()
			else:
				self.reload_()
				if not self.anya_done:
					self.fade_anya(self.anya_sprites[0])
				elif self.anya_done:
					self.reload_()
					self.reload_anya(self.anya_sprites[0])
					self.play_diags()
					self.draw_diag_rect()
					self.display_diag("Welcome to Anya's House!")
					pygame.display.update()
					break

	def intro(self):
		c = 0
		run = True
		exit_code = 0

		dialogues = ["Anya can read your mind.","Anya can tell whatever word you're thinking of!"]
		while run:
			clock.tick(60)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.display_diag("Anya had fun playing with you. Bye for now!")
					exit_code = 1
					run = False
				if event.type == pygame.MOUSEBUTTONDOWN:
					pos = pygame.mouse.get_pos()
					print(pos)

					if self.button_pos.collidepoint(pos):
						if c>len(dialogues)-1:
							run = False
						else:
							self.display_diag(dialogues[c])
							c+=1
		return exit_code

	def main(self):

		run = True

		length = ''
		n = 1
		c = 0

		input_loop = False
		matrix_input_loop = False
		transpose_matrix_input_loop = False

		transpose_columns_selected = []
		columns_selected = []
		exit_code = self.intro()

		if exit_code == 1:
			self.display_diag("Anya had fun playing with you. Bye for now!")
			pygame.quit()
		else:
			self.display_diag("Let's begin!!!")
			while run:
				clock.tick(60)
				for event in pygame.event.get():
					if event.type == pygame.QUIT:
						self.display_diag("Anya had fun playing with you. Bye for now!")
						run = False
					if event.type == pygame.MOUSEBUTTONDOWN:
						print(pygame.mouse.get_pos())
						if self.check_button_click(pygame.mouse.get_pos()):
							if length == '':
								self.reload_()
								self.reload_anya(self.anya_sprites[1])
								input_loop = True
								if c>1:
									c = 1
								self.display_diag("What is the length of your word?",c)
								self.display_input_prompt("Type a number: ")
								c+=1
							else:
								if input_loop:
									input_loop = False
									
									self.num_x = 229
									self.num_y = 452
									self.num_c = 0
									
									c = 0
									print(length)

								if not columns_selected:
									self.draw_matrix()
									matrix_input_loop = True
									self.display_diag(f"Which column number has the {n}th letter?")
									self.display_input_prompt("Type a number: ",'',1)
									n+=1
									c+=1

								elif columns_selected and len(columns_selected) != int(length):
									if c>1:
										c = 1
									self.display_diag(f"Which column number has the {n}th letter?",c)
									self.display_input_prompt("Type a number: ",'',1)
									n+=1

								elif columns_selected and len(columns_selected) == int(length):

									matrix_input_loop = False
									
									if not transpose_matrix_input_loop:
										transpose_matrix_input_loop = True
										self.num_x = 229
										self.num_y = 452
										self.num_c = 0
										c = 0
										n = 1
										self.draw_matrix_transpose(columns_selected)
										self.display_diag("You'll have to do it 1 more time now...")

									if not transpose_columns_selected:
										self.display_diag(f"Which column number has the {n}th letter?",c)
										self.display_input_prompt("Type a number: ",'',1)
										n+=1
										c+=1
									
									elif transpose_columns_selected and len(transpose_columns_selected) != int(length):

										if c>1:
											c = 1
										self.display_diag(f"Which column number has the {n}th letter?",c)
										self.display_input_prompt("Type a number: ",'',1)
										n+=1
									
									elif transpose_columns_selected and len(transpose_columns_selected) == int(length):
									
										self.reload_anya(self.anya_sprites[2])

										self.guesser.name_length = int(length)
										self.guesser.columns_selected = columns_selected
										self.guesser.transpose_columns_selected = transpose_columns_selected

										calculated_name = self.guesser.calc_name()

										self.display_diag(f"The word you were thinking of is \"{calculated_name}\" !!")
										
										length = ''
										n = 1
										c = 0
										
										self.num_x = 229
										self.num_y = 452
										self.num_c = 0
										
										columns_selected = []
										transpose_columns_selected = []
										
										transpose_matrix_input_loop = False


					if event.type == pygame.KEYDOWN and input_loop:
						if event.unicode.isdigit():
							self.display_input_prompt("Type a number: ",event.unicode)
							length+=str(event.unicode)

						elif event.key == pygame.K_BACKSPACE:
							self.display_input_prompt("Type a number: ",str(n),2)
							if length != '':
								length = length[:-1]
							if n != 1:
								n -=1

					elif event.type == pygame.KEYDOWN and matrix_input_loop:
						if event.unicode.isdigit():
							self.display_input_prompt("Type a number: ",event.unicode,1)
							columns_selected.append(int(event.unicode))

						elif event.key == pygame.K_BACKSPACE:
							self.display_input_prompt("Type a number: ",str(n), 3)
							if columns_selected:
								columns_selected.pop(-1)
					
					elif event.type == pygame.KEYDOWN and transpose_matrix_input_loop:
						if event.unicode.isdigit():
							self.display_input_prompt("Type a number: ",event.unicode,1)
							transpose_columns_selected.append(int(event.unicode))

						elif event.key == pygame.K_BACKSPACE:
							self.display_input_prompt("Type a number: ",str(n),3)
							if transpose_columns_selected:
								transpose_columns_selected.pop(-1)

Game()

#229 452