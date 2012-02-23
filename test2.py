#!/usr/bin/python
import panglery
p = panglery.Pangler()

@p.subscribe( needs = ['spam1'] )
def example_hook( p, spam1 ):
    print spam1

@p.subscribe( needs = ['condition'] )
def example_hook( p, condition ):
    if condition:
        print 'You pulled the truth trigger, full of happiness and good thoughts'
    else:
        print 'This trigger is false, you pulled it and nothing happened'

p.trigger( spam1 = 'eggs', condition = True )
p.trigger( condition = False )
