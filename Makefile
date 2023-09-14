##
## EPITECH PROJECT, 2023
## B-CNA-410-MPL-4-1-trade-owen.bolling
## File description:
## Makefile
##

NAME	=	trade

SRC		=	main.py

all:
	cp $(SRC) $(NAME)
	chmod 755 $(NAME)

clean:
	echo "Nothing to clean"

fclean:	clean
	rm $(NAME)	\

re:	fclean clean all