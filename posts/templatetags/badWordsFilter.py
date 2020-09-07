from django import template

register = template.Library()

@register.filter
def badWordsFilter(value, lisval):
	# print(lisval)
	# print()
	for word in lisval:
		if word in value:
			# print(word)
			value = value.replace(word,'*'*len(word))


	return value
