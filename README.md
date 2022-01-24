# Resume
> My professional resume in LaTeX, generated for multiple languages by using a simple templating language and YAML definitions for locales.

![license: GNU GPL v2](https://img.shields.io/badge/license-GNU_GPL_v2-brightgreen.svg) ![works: in my machine](https://img.shields.io/badge/works-in_my_machine-brightgreen.svg) [![license: live at anpep.co](https://img.shields.io/badge/live_at-anpep.co-blue.svg)](https://anpep.co/api/resume)
## Requirements
- Python >=3.9
- A normal TeX Live distribution (`texlive-latex-recommended`)
- *(Optional)* Language support packages (`texlive-lang-*`)
## Building the resume
```
$ git clone https://github.com/anpep/resume
$ cd resume && pip3 install -r requirements.txt
$ make clean all
```
## Editing the resume and adding more locales
The resume is generated from a single [YAML](https://yaml.org) document at `/locales/<locale>/locale.yaml` (e.g. for european spanish that's `/locales/es-ES/locale.yaml`). You can use LaTeX commands.

The LaTeX template is at `/tex/template.tex`.
## Template language syntax
Sample definition:
```yaml
Section:
	Value: Lorem ipsum
	List: [A B C D]
	Another-list:
		- My item 1
		- My item 2
		- My item 3
```
Sample TeX template:
```latex
% You can use the following syntax for simple string replacements:
[[Section Value]] dolor sit amet. This is my first list:

% You can iterate over lists.
% `Item` here can be a string, another list or an object.
\begin{itemize}
[[for Item in Section List]]
	\item [[Item]]
[[end for]]
\end{itemize}

% The following is particularly useful for lists that are
% distributed among two columns:
\begin{itemize}
[[for odd Item in Section Another-list]]
	% This will only include odd items (first, third, fifth...)
	% Note the `odd` modifier after the `for` keyword.
	\item [[Item]]
[[end for]]
\end{itemize}
\begin{itemize}
[[for even Item in Section Another-list]]
	% This will only include even items (second, fourth...)
	% Note the `even` modifier after the `for` keyword.
	\item [[Item]]
[[end for]]
\end{itemize}
```

## License
Sources in this repository are licensed under the GNU GPL v2 open-source license.
```
Copyright (c) 2022 Ángel Pérez <ap@anpep.co>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
```
