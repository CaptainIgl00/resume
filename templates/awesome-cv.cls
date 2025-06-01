%% Start of file `awesome-cv.cls'.
% ATS-Optimized Awesome CV Class File
% Based on Awesome-CV by Claud D. Park
% Optimized for ATS (Applicant Tracking Systems) compatibility

\ProvidesClass{awesome-cv}[2024/01/15 v2.0.0 ATS-Optimized Awesome Curriculum Vitae Class]
\NeedsTeXFormat{LaTeX2e}

%-------------------------------------------------------------------------------
%                Class options
%-------------------------------------------------------------------------------
\DeclareOption{draft}{\setlength\overfullrule{5pt}}
\DeclareOption{final}{\setlength\overfullrule{0pt}}
\DeclareOption*{%
  \PassOptionsToClass{\CurrentOption}{article}
}
\ProcessOptions\relax
\LoadClass{article}

%-------------------------------------------------------------------------------
%                3rd party packages - ATS optimized
%-------------------------------------------------------------------------------
\RequirePackage{array}
\RequirePackage{enumitem}
\RequirePackage{ragged2e}
\RequirePackage{geometry}
\RequirePackage{fancyhdr}
\RequirePackage{xcolor}
\RequirePackage{ifxetex}
\RequirePackage{xifthen}
\RequirePackage{xstring}
\RequirePackage{etoolbox}
\RequirePackage{setspace}
\RequirePackage[quiet]{fontspec}
\defaultfontfeatures{Ligatures=TeX}
\RequirePackage{unicode-math}
% Minimal icon usage for ATS compatibility
\RequirePackage{fontawesome5}
\RequirePackage{roboto}
\RequirePackage[default,opentype]{sourcesanspro}
\RequirePackage{parskip}
% ATS-friendly hyperlinks
\RequirePackage[hidelinks,unicode,pdfpagelabels=false]{hyperref}
\hypersetup{%
  pdftitle={Resume},
  pdfauthor={},
  pdfsubject={Curriculum Vitae},
  pdfkeywords={resume,cv}
}
\RequirePackage{bookmark}

%-------------------------------------------------------------------------------
%                ATS-Optimized Layout Configuration
%-------------------------------------------------------------------------------
% Larger margins for better text parsing
\geometry{left=2.5cm, top=2.0cm, right=2.5cm, bottom=2.5cm, footskip=.8cm}

% Clean header & footer
\fancyhfoffset{0em}
\renewcommand{\headrulewidth}{0pt}
\fancyhf{}
\pagestyle{fancy}

%-------------------------------------------------------------------------------
%                ATS-Friendly Color Configuration
%-------------------------------------------------------------------------------
% Simplified color scheme for ATS compatibility
\definecolor{white}{HTML}{FFFFFF}
\definecolor{black}{HTML}{000000}
\definecolor{darkgray}{HTML}{2B2B2B}
\definecolor{gray}{HTML}{4A4A4A}
\definecolor{lightgray}{HTML}{777777}
\definecolor{mediumgray}{HTML}{666666}

% ATS-friendly primary color (dark blue)
\definecolor{ats-blue}{HTML}{1F4788}
\definecolor{ats-darkblue}{HTML}{0F2C4C}

% Text colors optimized for readability and ATS parsing
\colorlet{text}{black}
\colorlet{graytext}{mediumgray}
\colorlet{lighttext}{gray}
\colorlet{sectiondivider}{mediumgray}
\colorlet{awesome}{ats-blue}

% Disable section color highlighting for ATS compatibility
\newbool{acvSectionColorHighlight}
\setbool{acvSectionColorHighlight}{false}

\def\@sectioncolor#1#2#3{%
  \ifbool{acvSectionColorHighlight}{{\color{awesome}#1#2#3}}{#1#2#3}%
}

%-------------------------------------------------------------------------------
%                ATS-Optimized Font Configuration
%-------------------------------------------------------------------------------
\newcommand*{\headerfont}{\sourcesanspro}
\newcommand*{\headerfontlight}{\sourcesansprolight}
\newcommand*{\footerfont}{\sourcesanspro}
\newcommand*{\bodyfont}{\sourcesanspro}
\newcommand*{\bodyfontlight}{\sourcesanspro}

%-------------------------------------------------------------------------------
%                ATS-Optimized Styles
%-------------------------------------------------------------------------------
% Larger, clearer fonts for better ATS parsing
\newcommand*{\headerfirstnamestyle}[1]{{\fontsize{24pt}{1.2em}\headerfont\bfseries\color{text} #1}}
\newcommand*{\headerlastnamestyle}[1]{{\fontsize{24pt}{1.2em}\headerfont\bfseries\color{text} #1}}
\newcommand*{\headerpositionstyle}[1]{{\fontsize{12pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\headeraddressstyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\headersocialstyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\headerquotestyle}[1]{{\fontsize{11pt}{1.3em}\bodyfont\color{text} #1}}
\newcommand*{\footerstyle}[1]{{\fontsize{9pt}{1.2em}\footerfont\color{lighttext} #1}}
\newcommand*{\sectionstyle}[1]{{\fontsize{14pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\subsectionstyle}[1]{{\fontsize{12pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\paragraphstyle}{\fontsize{10pt}{1.3em}\bodyfont\color{text}}

% Entry styles optimized for ATS
\newcommand*{\entrytitlestyle}[1]{{\fontsize{11pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\entrypositionstyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\entrydatestyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\entrylocationstyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\descriptionstyle}[1]{{\fontsize{10pt}{1.3em}\bodyfont\color{text} #1}}

% Subentry styles
\newcommand*{\subentrytitlestyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{text} #1}}
\newcommand*{\subentrypositionstyle}[1]{{\fontsize{9pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\subentrydatestyle}[1]{{\fontsize{9pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\subentrylocationstyle}[1]{{\fontsize{9pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\subdescriptionstyle}[1]{{\fontsize{9pt}{1.3em}\bodyfont\color{text} #1}}

% Honor/Award styles
\newcommand*{\honortitlestyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{text} #1}}
\newcommand*{\honorpositionstyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\honordatestyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\honorlocationstyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}

% Skill styles
\newcommand*{\skilltypestyle}[1]{{\fontsize{11pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\skillsetstyle}[1]{{\fontsize{10pt}{1.3em}\bodyfont\color{text} #1}}

% Cover letter styles
\newcommand*{\lettersectionstyle}[1]{{\fontsize{13pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\recipientaddressstyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\recipienttitlestyle}[1]{{\fontsize{11pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\lettertitlestyle}[1]{{\fontsize{11pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\letterdatestyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}
\newcommand*{\lettertextstyle}{\fontsize{10pt}{1.4em}\bodyfont\color{text}}
\newcommand*{\letternamestyle}[1]{{\fontsize{11pt}{1.2em}\bodyfont\bfseries\color{text} #1}}
\newcommand*{\letterenclosurestyle}[1]{{\fontsize{10pt}{1.2em}\bodyfont\color{graytext} #1}}

%-------------------------------------------------------------------------------
%                Personal Information Commands
%-------------------------------------------------------------------------------
% Photo ID with minimal styling
\newcommand{\photo}[2][circle,edge,left]{%
  \def\@photo{#2}
  \@for\tmp:=#1\do{%
    \ifthenelse{\equal{\tmp}{circle} \or \equal{\tmp}{rectangle}}%
      {\let\@photoshape\tmp}{}%
    \ifthenelse{\equal{\tmp}{edge} \or \equal{\tmp}{noedge}}%
      {\let\@photoedge\tmp}{}%
    \ifthenelse{\equal{\tmp}{left} \or \equal{\tmp}{right}}%
      {\let\@photoalign\tmp}{}%
  }%
}
\def\@photoshape{circle}
\def\@photoedge{edge}
\def\@photoalign{left}

% Personal information commands
\newcommand*{\name}[2]{\def\@firstname{#1}\def\@lastname{#2}}
\newcommand*{\firstname}[1]{\def\@firstname{#1}}
\newcommand*{\lastname}[1]{\def\@lastname{#1}}
\newcommand*{\familyname}[1]{\def\@lastname{#1}}
\def\@familyname{\@lastname}
\newcommand*{\address}[1]{\def\@address{#1}}
\newcommand*{\position}[1]{\def\@position{#1}}

% Contact information
\newcommand*{\mobile}[1]{
  \def\@mobile{#1}
  \def\@teluri{tel:\@mobile}
  \StrDel{\@teluri}{ }[\@teluri]%
  \StrDel{\@teluri}{-}[\@teluri]%
  \StrDel{\@teluri}{(}[\@teluri]%
  \StrDel{\@teluri}{)}[\@teluri]%
}
\newcommand*{\email}[1]{\def\@email{#1}}
\newcommand*{\homepage}[1]{\def\@homepage{#1}}
\newcommand*{\github}[1]{\def\@github{#1}}
\newcommand*{\gitlab}[1]{\def\@gitlab{#1}}
\newcommand*{\linkedin}[1]{\def\@linkedin{#1}}
\newcommand*{\twitter}[1]{\def\@twitter{#1}}

% Additional information
\newcommand*{\extrainfo}[1]{\def\@extrainfo{#1}}
\renewcommand*{\quote}[1]{\def\@quote{#1}}

%-------------------------------------------------------------------------------
%                Helper Commands - ATS Optimized
%-------------------------------------------------------------------------------
\newcommand{\acvHeaderNameDelim}{\space}
\newcommand{\acvHeaderAfterNameSkip}{1.0mm}
\newcommand{\acvHeaderAfterPositionSkip}{1.0mm}
\newcommand{\acvHeaderAfterAddressSkip}{0.5mm}
\newcommand{\acvHeaderIconSep}{\space}
\newcommand{\acvHeaderSocialSep}{\quad|\quad}
\newcommand{\acvHeaderAfterSocialSkip}{4mm}
\newcommand{\acvHeaderAfterQuoteSkip}{3mm}

\newcommand{\acvSectionTopSkip}{4mm}
\newcommand{\acvSectionContentTopSkip}{3mm}

%-------------------------------------------------------------------------------
%                Utilities
%-------------------------------------------------------------------------------
\newcolumntype{L}[1]{>{\raggedright\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{C}[1]{>{\centering\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}
\newcolumntype{R}[1]{>{\raggedleft\let\newline\\\arraybackslash\hspace{0pt}}m{#1}}

\def\vhrulefill#1{\leavevmode\leaders\hrule\@height#1\hfill \kern\z@}
\newcommand*{\ifempty}[3]{\ifthenelse{\isempty{#1}}{#2}{#3}}

%-------------------------------------------------------------------------------
%                ATS-Optimized CV Structure Commands
%-------------------------------------------------------------------------------
% Simplified header for better ATS parsing
\newcommand*{\makecvheader}[1][L]{%
  \begin{center}
    \headerfirstnamestyle{\@firstname}\headerlastnamestyle{{}\acvHeaderNameDelim\@lastname}%
    \\[\acvHeaderAfterNameSkip]%
    \ifthenelse{\isundefined{\@position}}{}{\headerpositionstyle{\@position\\[\acvHeaderAfterPositionSkip]}}%
    \ifthenelse{\isundefined{\@address}}{}{\headeraddressstyle{\@address\\[\acvHeaderAfterAddressSkip]}}%
    \headersocialstyle{%
      \newbool{isstart}%
      \setbool{isstart}{true}%
      \ifthenelse{\isundefined{\@mobile}}%
        {}%
        {%
          \@mobile%
          \setbool{isstart}{false}%
        }%
      \ifthenelse{\isundefined{\@email}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \ifthenelse{\isundefined{\emailicon}}{}{\emailicon~}\href{mailto:\@email}{\@email}%
        }%
      \ifthenelse{\isundefined{\@github}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \ifthenelse{\isundefined{\githubicon}}{}{\githubicon~}\href{https://github.com/\@github}{github.com/\@github}%
        }%
      \ifthenelse{\isundefined{\@linkedin}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \ifthenelse{\isundefined{\linkedinicon}}{}{\linkedinicon~}\href{https://linkedin.com/in/\@linkedin}{linkedin.com/in/\@linkedin}%
        }%
      \ifthenelse{\isundefined{\@extrainfo}}%
        {}%
        {%
          \ifbool{isstart}{\setbool{isstart}{false}}{\acvHeaderSocialSep}%
          \@extrainfo%
        }%
    } \\[\acvHeaderAfterSocialSkip]%
    \ifthenelse{\isundefined{\@quote}}%
      {}%
      {\headerquotestyle{\@quote\\}\vspace{\acvHeaderAfterQuoteSkip}}%
  \end{center}
}

% Simple section divider for ATS
\newcommand{\cvsection}[1]{%
  \vspace{\acvSectionTopSkip}
  \sectionstyle{#1}
  \phantomsection
  \color{sectiondivider}\vhrulefill{0.5pt}
}

\newcommand{\cvsubsection}[1]{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-2mm}
  \subsectionstyle{#1}
  \phantomsection
}

\newenvironment{cvparagraph}{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-2mm}
  \paragraphstyle
}{%
  \par
  \vspace{2mm}
}

% ATS-friendly entry format
\newenvironment{cventries}{%
  \vspace{\acvSectionContentTopSkip}
  \begin{center}
}{%
  \end{center}
}

\newcommand*{\cventry}[5]{%
  \vspace{-1.0mm}
  \setlength\tabcolsep{0pt}
  \setlength{\extrarowheight}{0pt}
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} L{\textwidth - 5.0cm} R{5.0cm}}
    \ifempty{#2#3}
      {\entrypositionstyle{#1} & \entrydatestyle{#4} \\}
      {\entrytitlestyle{#2} & \entrylocationstyle{#3} \\
      \entrypositionstyle{#1} & \entrydatestyle{#4} \\}
    \ifstrempty{#5}
      {}
      {\multicolumn{2}{L{\textwidth}}{\descriptionstyle{#5}} \\}
  \end{tabular*}%
}

% Skills environment optimized for ATS parsing
\newenvironment{cvskills}{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-1.0mm}
  \begin{center}
    \setlength\tabcolsep{2ex}
    \setlength{\extrarowheight}{0pt}
    \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} L{0.25\textwidth} L{0.75\textwidth}}
}{%
    \end{tabular*}
  \end{center}
}

\newcommand*{\cvskill}[2]{%
	\skilltypestyle{#1} & \skillsetstyle{#2} \\
}

% Clean itemize for ATS
\newenvironment{cvitems}{%
  \vspace{-3.0mm}
  \begin{justify}
  \begin{itemize}[leftmargin=2ex, nosep, noitemsep]
    \setlength{\parskip}{0pt}
    \renewcommand{\labelitemi}{\textbullet}
}{%
  \end{itemize}
  \end{justify}
  \vspace{-3.0mm}
}

% Honor/Award environment
\newenvironment{cvhonors}{%
  \vspace{\acvSectionContentTopSkip}
  \vspace{-1mm}
  \begin{center}
    \setlength\tabcolsep{0pt}
    \setlength{\extrarowheight}{0pt}
    \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} L{0.15\textwidth} L{\textwidth - 3.5cm} R{2.5cm}}
}{%
    \end{tabular*}
  \end{center}
}

\newcommand*{\cvhonor}[4]{%
  \honordatestyle{#4} & \honorpositionstyle{#1}\ifempty{#2}{}{, } \honortitlestyle{#2} & \honorlocationstyle{#3} \\
}

%-------------------------------------------------------------------------------
%                Cover Letter Commands (simplified)
%-------------------------------------------------------------------------------
\newenvironment{cvletter}{%
  \lettertextstyle
}{}

\newcommand{\lettersection}[1]{%
  \par\addvspace{2.5ex}
  \phantomsection{}
  \lettersectionstyle{#1}
  \color{sectiondivider}\vhrulefill{0.5pt}
  \par\nobreak\addvspace{0.4ex}
  \lettertextstyle
}

% Letter header and closing
\newcommand*{\recipient}[2]{\def\@recipientname{#1}\def\@recipientaddress{#2}}
\newcommand*{\letterdate}[1]{\def\@letterdate{#1}}
\newcommand*{\letteropening}[1]{\def\@letteropening{#1}}
\newcommand*{\letterclosing}[1]{\def\@letterclosing{#1}}

\newcommand*{\makelettertitle}{%
  \vspace{8.4mm}
  \setlength\tabcolsep{0pt}
  \setlength{\extrarowheight}{0pt}
  \begin{tabular*}{\textwidth}{@{\extracolsep{\fill}} L{\textwidth - 4.5cm} R{4.5cm}}
    \recipienttitlestyle{\@recipientname} & \letterdatestyle{\@letterdate}
  \end{tabular*}
  \begin{singlespace}
    \recipientaddressstyle{\@recipientaddress} \\\\
  \end{singlespace}
  \lettertextstyle{\@letteropening}
}

\newcommand*{\makeletterclosing}{%
  \vspace{3.4mm}
  \lettertextstyle{\@letterclosing} \\\\
  \letternamestyle{\@firstname\ \@lastname}
}
