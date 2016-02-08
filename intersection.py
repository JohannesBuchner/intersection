"""


"""
from sympy import *

# equations

equations = {}

x, y, z = symbols('x, y, z')
a, b, c = symbols('a, b, c')
x0, y0, z0 = symbols('x0, y0, z0')
R, t = symbols('R, t')
k, l = symbols('k, l')
phi, theta = symbols('phi, theta')

# cartesian coordinates
line_x = t + x0  
line_y = k*t + y0
line_z = l*t + z0
line_cartesian = [(x,line_x), (y,line_y), (z,line_z)]

# spherical coordinates
# t, phi, theta
line_x = x0 + t * sin(theta) * cos(phi)
line_y = y0 + t * sin(theta) * sin(phi)
line_z = z0 + t * cos(theta)
line_spherical = [(x,line_x), (y,line_y), (z,line_z)]
equations['line'] = {'cartesian': line_cartesian, 'spherical': line_spherical}

# sphere + ellipsoid
sphere = (x/R)**2 + (y/R)**2 + (z/R)**2 - 1
ellipsoid = (x/a)**2 + (y/b)**2 + (z/c)**2 - 1
equations['sphere'] = {'cartesian': sphere}
equations['ellipsoid'] = {'cartesian': ellipsoid}

# cone + cylinder
cone = (x**2 + y**2)/c**2 - z**2
cylinder = (x/a)**2 + (y/b)**2 - 1
equations['cone'] = {'cartesian': cone}
equations['cylinder'] = {'cartesian': cylinder}

# other quadratic surface objects
hyperboloid = (x/a)**2 + (y/b)**2 - (z/c)**2 - 1
equations['hyperboloid'] = {'cartesian': hyperboloid}
hyperboloid2 = -(x/a)**2 - (y/b)**2 + (z/c)**2 - 1
equations['hyperboloid_twosheets'] = {'cartesian': hyperboloid2}

ell_paraboloid = (x/a)**2 + (y/b)**2 - z/c
equations['elliptical_paraboloid'] = {'cartesian': ell_paraboloid}
hyp_paraboloid = (x/a)**2 - (y/b)**2 - z/c
equations['hyperbolical_paraboloid'] = {'cartesian': hyp_paraboloid}

# plane 
plane = a*x + b*y + c*z
equations['plane'] = {'cartesian': plane}

#otherline = a*x + b*y + c*z
#equations['otherline'] = {'cartesian': otherline}

combinations = [('line', obj) for obj in equations.keys() if obj != 'line']

# 2d intersections
line_x = t + x0  
line_y = k*t + y0
line2d_cartesian =  [(x,line_x), (y,line_y)]

line_x = x0 + t * cos(phi)
line_y = y0 + t * sin(phi)
line2d_spherical = [(x,line_x), (y,line_y)]
equations['2d_line'] = {'cartesian': line2d_cartesian, 'spherical': line2d_spherical}

# circle 
circle = (x/R)**2 + (y/R)**2 - 1
ellipse = (x/a)**2 + (y/b)**2 - 1
equations['circle'] = {'cartesian': circle}
equations['ellipse'] = {'cartesian': ellipse}

combinations += [('2d_line', 'circle'), ('2d_line', 'ellipse')]

combinations = combinations[::-1]


#from sympy.printing.mathml import mathml
#def _mathml(expression):
#	return '<math xmlns="http://www.w3.org/1998/Math/MathML">' + "\n" + mathml(expression) + "\n</math>\n"
from io import BytesIO
from sympy.printing.preview import preview
from sympy.printing.latex import latex
from sympy.printing.ccode import ccode
filei = 1
def _mathml(expression):
	global filei
	filename = 'eq%d.png' % filei
	filei = filei + 1
	preview(expression, output='png', viewer='file', filename=filename)
	latexstr = latex(expression)
	return '<img src="%s" alt="%s" />' % (filename, latexstr)

def _simplify(expression):
	s = simplify(expression)
	f = factor(expression)
	e = expand(expression)
	return min((len(str(expression)), expression), (len(str(s)), s), (len(str(f)), f), (len(str(e)), e))[1]

findex = open('index.html', 'w')
title = 'Line-Intersection formulae'
header = open('header.html', 'r').read()
findex.write(header % dict(title=title))
findex.write("<h2>%s</h2>\n" % (title))
findex.write("""<p>Ray tracing formulas for various 2d and 3d objects
were derived using the computer-algebra system sympy.</p>\n""")
findex.write("""<p>The collection currently contains:</p>\n""")
findex.write("<ul>\n")

for a, b in combinations:
	filename = 'intersection_%s_%s.html' % (a, b)
	fout = open(filename, 'w')
	title = '%s - %s intersection' % (a, b)
	fout.write(header % dict(title=title))
	fout.write("<h2>%s</h2>\n" % (title))
	findex.write("<li><a href='%s'>%s</a></li>\n" % (filename, title))
	findex.flush()
	print
	for an in sorted(equations[a].keys()):
		ai = equations[a][an]
		for bn in sorted(equations[b].keys()):
			bi = equations[b][bn]
			fout.write("<h4>Equation for %s (%s)</h4>\n" % (a, an))
			fout.write("<ul>\n")
			for k, v in ai:
				fout.write("<li>%s: %s</li>\n" % (k, _mathml(v)))
			fout.write("</ul>\n")
			fout.write("<h4>Equation for %s (%s)</h4>\n" % (b, bn))
			fout.write("<p>Assumed to be centred at 0, the coordinate system origin.</p>\n")
			fout.write("0=%s\n" % _mathml(bi))
			
			# compute intersection points
			fout.write("<h4>Intersection solutions</h4>\n")
			fout.write("<p>Parametric solution (t). Solutions were derived automatically using sympy.</p>\n")
			print 'solving %s (%s|%s)...' % (title, an, bn)
			solutions = solve(bi.subs(ai), t)
			print 'solved.'
			if len(solutions) == 0:
				fout.write("none.\n")
			else:
				fout.write("<ul>")
				for i, sol in enumerate(solutions):
					fout.write("<li>%s</li>\n" % _mathml(sol))
					# ccode(sol, assign_to='sol%d' % (i+1))
				fout.write("</ul>")
			
			fout.write("<p>Points in cartesian coordinates (x, y, z)</p>\n")
			fout.write("<ul>")
			for i, sol in enumerate(solutions):
				fout.write("<li><ul>")
				for k, v in ai:
					fout.write("<li>%s: %s</li>\n" % (k, _mathml(v.subs(t, sol))))
				fout.write("</ul></li>")
			fout.write("</ul>")
			fout.write("<h5>C Code</h5>\n")
			for i, sol in enumerate(solutions):
				for k, v in ai:
					fout.write("<pre>%s</pre>\n" % ccode(v.subs(t, sol), assign_to=k))
				
			if len(solutions) == 2:
				sola, solb = solutions
				# compute distance inside
				
				distance = _simplify(Abs(sola - solb))
				fout.write("<h4>Distance inside</h4>\n")
				fout.write("<p>Distance between crossing points.</p>\n")
				fout.write("%s\n" % _mathml(distance))
				fout.write("<h4>C Code</h4>\n")
				for i, sol in enumerate(solutions):
					fout.write("<pre>%s</pre>" % ccode(sol, assign_to='sol%d' % (i+1)))
				fout.write("<pre>%s</pre>" % ccode(distance, assign_to="distance"))

			if len(solutions) == 1:
				sol = solutions[0]
				fout.write("<h4>C Code</h4>\n")
				fout.write("<pre>%s</pre>" % ccode(sol, assign_to="sol"))
			fout.write("<hr/>\n")
	
	
	


