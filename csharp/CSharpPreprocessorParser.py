# Generated from .\csharp\CSharpPreprocessorParser.g4 by ANTLR 4.9.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

import java.util.Stack;
import java.util.HashSet;

def serializedATN():
    with StringIO() as buf:
        buf.write("\3\u608b\ua72a\u8133\ub9ed\u417c\u3be7\u7786\u5964\3\u00c8")
        buf.write("\u0082\4\2\t\2\4\3\t\3\4\4\t\4\3\2\3\2\3\2\3\2\3\2\3\2")
        buf.write("\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2(\n")
        buf.write("\2\3\2\3\2\5\2,\n\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\3\2\3\2\3\2\3\2\5\2=\n\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\5\2D\n\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3\2\3")
        buf.write("\2\3\2\3\2\5\2S\n\2\3\3\3\3\3\4\3\4\3\4\3\4\3\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\5\4g\n\4\3\4\3")
        buf.write("\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4\3\4")
        buf.write("\3\4\3\4\3\4\3\4\3\4\7\4}\n\4\f\4\16\4\u0080\13\4\3\4")
        buf.write("\2\3\6\5\2\4\6\2\3\3\3\u00c6\u00c6\2\u0097\2R\3\2\2\2")
        buf.write("\4T\3\2\2\2\6f\3\2\2\2\b\t\7\u00b9\2\2\t\n\7\u00c5\2\2")
        buf.write("\n\13\5\4\3\2\13\f\b\2\1\2\fS\3\2\2\2\r\16\7\u00ba\2\2")
        buf.write("\16\17\7\u00c5\2\2\17\20\5\4\3\2\20\21\b\2\1\2\21S\3\2")
        buf.write("\2\2\22\23\7\66\2\2\23\24\5\6\4\2\24\25\5\4\3\2\25\26")
        buf.write("\b\2\1\2\26S\3\2\2\2\27\30\7\u00bb\2\2\30\31\5\6\4\2\31")
        buf.write("\32\5\4\3\2\32\33\b\2\1\2\33S\3\2\2\2\34\35\7&\2\2\35")
        buf.write("\36\5\4\3\2\36\37\b\2\1\2\37S\3\2\2\2 !\7\u00bc\2\2!\"")
        buf.write("\5\4\3\2\"#\b\2\1\2#S\3\2\2\2$+\7\u00bd\2\2%\'\7\u00b8")
        buf.write("\2\2&(\7]\2\2\'&\3\2\2\2\'(\3\2\2\2(,\3\2\2\2),\7 \2\2")
        buf.write("*,\7\u00c4\2\2+%\3\2\2\2+)\3\2\2\2+*\3\2\2\2,-\3\2\2\2")
        buf.write("-.\5\4\3\2./\b\2\1\2/S\3\2\2\2\60\61\7\u00be\2\2\61\62")
        buf.write("\7\u00c7\2\2\62\63\5\4\3\2\63\64\b\2\1\2\64S\3\2\2\2\65")
        buf.write("\66\7\u00bf\2\2\66\67\7\u00c7\2\2\678\5\4\3\289\b\2\1")
        buf.write("\29S\3\2\2\2:<\7\u00c0\2\2;=\7\u00c7\2\2<;\3\2\2\2<=\3")
        buf.write("\2\2\2=>\3\2\2\2>?\5\4\3\2?@\b\2\1\2@S\3\2\2\2AC\7\u00c1")
        buf.write("\2\2BD\7\u00c7\2\2CB\3\2\2\2CD\3\2\2\2DE\3\2\2\2EF\5\4")
        buf.write("\3\2FG\b\2\1\2GS\3\2\2\2HI\7\u00c2\2\2IJ\7\u00c7\2\2J")
        buf.write("K\5\4\3\2KL\b\2\1\2LS\3\2\2\2MN\7\u00c3\2\2NO\7\u00c7")
        buf.write("\2\2OP\5\4\3\2PQ\b\2\1\2QS\3\2\2\2R\b\3\2\2\2R\r\3\2\2")
        buf.write("\2R\22\3\2\2\2R\27\3\2\2\2R\34\3\2\2\2R \3\2\2\2R$\3\2")
        buf.write("\2\2R\60\3\2\2\2R\65\3\2\2\2R:\3\2\2\2RA\3\2\2\2RH\3\2")
        buf.write("\2\2RM\3\2\2\2S\3\3\2\2\2TU\t\2\2\2U\5\3\2\2\2VW\b\4\1")
        buf.write("\2WX\7b\2\2Xg\b\4\1\2YZ\7,\2\2Zg\b\4\1\2[\\\7\u00c5\2")
        buf.write("\2\\g\b\4\1\2]^\7\u0083\2\2^_\5\6\4\2_`\7\u0084\2\2`a")
        buf.write("\b\4\1\2ag\3\2\2\2bc\7\u0091\2\2cd\5\6\4\7de\b\4\1\2e")
        buf.write("g\3\2\2\2fV\3\2\2\2fY\3\2\2\2f[\3\2\2\2f]\3\2\2\2fb\3")
        buf.write("\2\2\2g~\3\2\2\2hi\f\6\2\2ij\7\u009e\2\2jk\5\6\4\7kl\b")
        buf.write("\4\1\2l}\3\2\2\2mn\f\5\2\2no\7\u009f\2\2op\5\6\4\6pq\b")
        buf.write("\4\1\2q}\3\2\2\2rs\f\4\2\2st\7\u009b\2\2tu\5\6\4\5uv\b")
        buf.write("\4\1\2v}\3\2\2\2wx\f\3\2\2xy\7\u009c\2\2yz\5\6\4\4z{\b")
        buf.write("\4\1\2{}\3\2\2\2|h\3\2\2\2|m\3\2\2\2|r\3\2\2\2|w\3\2\2")
        buf.write("\2}\u0080\3\2\2\2~|\3\2\2\2~\177\3\2\2\2\177\7\3\2\2\2")
        buf.write("\u0080~\3\2\2\2\n\'+<CRf|~")
        return buf.getvalue()


class CSharpPreprocessorParser ( Parser ):

    grammarFileName = "CSharpPreprocessorParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'\u00EF\u00BB\u00BF'", "<INVALID>", "'/***/'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'#'", "'abstract'", "'add'", "'alias'", "'__arglist'", 
                     "'as'", "'ascending'", "'async'", "'await'", "'base'", 
                     "'bool'", "'break'", "'by'", "'byte'", "'case'", "'catch'", 
                     "'char'", "'checked'", "'class'", "'const'", "'continue'", 
                     "'decimal'", "'default'", "'delegate'", "'descending'", 
                     "'do'", "'double'", "'dynamic'", "'else'", "'enum'", 
                     "'equals'", "'event'", "'explicit'", "'extern'", "'false'", 
                     "'finally'", "'fixed'", "'float'", "'for'", "'foreach'", 
                     "'from'", "'get'", "'goto'", "'group'", "'if'", "'implicit'", 
                     "'in'", "'int'", "'interface'", "'internal'", "'into'", 
                     "'is'", "'join'", "'let'", "'lock'", "'long'", "'nameof'", 
                     "'namespace'", "'new'", "'null'", "'object'", "'on'", 
                     "'operator'", "'orderby'", "'out'", "'override'", "'params'", 
                     "'partial'", "'private'", "'protected'", "'public'", 
                     "'readonly'", "'ref'", "'remove'", "'return'", "'sbyte'", 
                     "'sealed'", "'select'", "'set'", "'short'", "'sizeof'", 
                     "'stackalloc'", "'static'", "'string'", "'struct'", 
                     "'switch'", "'this'", "'throw'", "'true'", "'try'", 
                     "'typeof'", "'uint'", "'ulong'", "'unchecked'", "'unmanaged'", 
                     "'unsafe'", "'ushort'", "'using'", "'var'", "'virtual'", 
                     "'void'", "'volatile'", "'when'", "'where'", "'while'", 
                     "'yield'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'{'", "'}'", 
                     "'['", "']'", "'('", "')'", "'.'", "','", "':'", "';'", 
                     "'+'", "'-'", "'*'", "'/'", "'%'", "'&'", "'|'", "'^'", 
                     "'!'", "'~'", "'='", "'<'", "'>'", "'?'", "'::'", "'??'", 
                     "'++'", "'--'", "'&&'", "'||'", "'->'", "'=='", "'!='", 
                     "'<='", "'>='", "'+='", "'-='", "'*='", "'/='", "'%='", 
                     "'&='", "'|='", "'^='", "'<<'", "'<<='", "'??='", "'..'", 
                     "'{{'", "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "'define'", "'undef'", "'elif'", 
                     "'endif'", "'line'", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'hidden'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "'}}'" ]

    symbolicNames = [ "<INVALID>", "BYTE_ORDER_MARK", "SINGLE_LINE_DOC_COMMENT", 
                      "EMPTY_DELIMITED_DOC_COMMENT", "DELIMITED_DOC_COMMENT", 
                      "SINGLE_LINE_COMMENT", "DELIMITED_COMMENT", "WHITESPACES", 
                      "SHARP", "ABSTRACT", "ADD", "ALIAS", "ARGLIST", "AS", 
                      "ASCENDING", "ASYNC", "AWAIT", "BASE", "BOOL", "BREAK", 
                      "BY", "BYTE", "CASE", "CATCH", "CHAR", "CHECKED", 
                      "CLASS", "CONST", "CONTINUE", "DECIMAL", "DEFAULT", 
                      "DELEGATE", "DESCENDING", "DO", "DOUBLE", "DYNAMIC", 
                      "ELSE", "ENUM", "EQUALS", "EVENT", "EXPLICIT", "EXTERN", 
                      "FALSE", "FINALLY", "FIXED", "FLOAT", "FOR", "FOREACH", 
                      "FROM", "GET", "GOTO", "GROUP", "IF", "IMPLICIT", 
                      "IN", "INT", "INTERFACE", "INTERNAL", "INTO", "IS", 
                      "JOIN", "LET", "LOCK", "LONG", "NAMEOF", "NAMESPACE", 
                      "NEW", "NULL_", "OBJECT", "ON", "OPERATOR", "ORDERBY", 
                      "OUT", "OVERRIDE", "PARAMS", "PARTIAL", "PRIVATE", 
                      "PROTECTED", "PUBLIC", "READONLY", "REF", "REMOVE", 
                      "RETURN", "SBYTE", "SEALED", "SELECT", "SET", "SHORT", 
                      "SIZEOF", "STACKALLOC", "STATIC", "STRING", "STRUCT", 
                      "SWITCH", "THIS", "THROW", "TRUE", "TRY", "TYPEOF", 
                      "UINT", "ULONG", "UNCHECKED", "UNMANAGED", "UNSAFE", 
                      "USHORT", "USING", "VAR", "VIRTUAL", "VOID", "VOLATILE", 
                      "WHEN", "WHERE", "WHILE", "YIELD", "IDENTIFIER", "LITERAL_ACCESS", 
                      "INTEGER_LITERAL", "HEX_INTEGER_LITERAL", "BIN_INTEGER_LITERAL", 
                      "REAL_LITERAL", "CHARACTER_LITERAL", "REGULAR_STRING", 
                      "VERBATIUM_STRING", "INTERPOLATED_REGULAR_STRING_START", 
                      "INTERPOLATED_VERBATIUM_STRING_START", "OPEN_BRACE", 
                      "CLOSE_BRACE", "OPEN_BRACKET", "CLOSE_BRACKET", "OPEN_PARENS", 
                      "CLOSE_PARENS", "DOT", "COMMA", "COLON", "SEMICOLON", 
                      "PLUS", "MINUS", "STAR", "DIV", "PERCENT", "AMP", 
                      "BITWISE_OR", "CARET", "BANG", "TILDE", "ASSIGNMENT", 
                      "LT", "GT", "INTERR", "DOUBLE_COLON", "OP_COALESCING", 
                      "OP_INC", "OP_DEC", "OP_AND", "OP_OR", "OP_PTR", "OP_EQ", 
                      "OP_NE", "OP_LE", "OP_GE", "OP_ADD_ASSIGNMENT", "OP_SUB_ASSIGNMENT", 
                      "OP_MULT_ASSIGNMENT", "OP_DIV_ASSIGNMENT", "OP_MOD_ASSIGNMENT", 
                      "OP_AND_ASSIGNMENT", "OP_OR_ASSIGNMENT", "OP_XOR_ASSIGNMENT", 
                      "OP_LEFT_SHIFT", "OP_LEFT_SHIFT_ASSIGNMENT", "OP_COALESCING_ASSIGNMENT", 
                      "OP_RANGE", "DOUBLE_CURLY_INSIDE", "OPEN_BRACE_INSIDE", 
                      "REGULAR_CHAR_INSIDE", "VERBATIUM_DOUBLE_QUOTE_INSIDE", 
                      "DOUBLE_QUOTE_INSIDE", "REGULAR_STRING_INSIDE", "VERBATIUM_INSIDE_STRING", 
                      "CLOSE_BRACE_INSIDE", "FORMAT_STRING", "DIRECTIVE_WHITESPACES", 
                      "DIGITS", "DEFINE", "UNDEF", "ELIF", "ENDIF", "LINE", 
                      "ERROR", "WARNING", "REGION", "ENDREGION", "PRAGMA", 
                      "NULLABLE", "DIRECTIVE_HIDDEN", "CONDITIONAL_SYMBOL", 
                      "DIRECTIVE_NEW_LINE", "TEXT", "DOUBLE_CURLY_CLOSE_INSIDE" ]

    RULE_preprocessor_directive = 0
    RULE_directive_new_line_or_sharp = 1
    RULE_preprocessor_expression = 2

    ruleNames =  [ "preprocessor_directive", "directive_new_line_or_sharp", 
                   "preprocessor_expression" ]

    EOF = Token.EOF
    BYTE_ORDER_MARK=1
    SINGLE_LINE_DOC_COMMENT=2
    EMPTY_DELIMITED_DOC_COMMENT=3
    DELIMITED_DOC_COMMENT=4
    SINGLE_LINE_COMMENT=5
    DELIMITED_COMMENT=6
    WHITESPACES=7
    SHARP=8
    ABSTRACT=9
    ADD=10
    ALIAS=11
    ARGLIST=12
    AS=13
    ASCENDING=14
    ASYNC=15
    AWAIT=16
    BASE=17
    BOOL=18
    BREAK=19
    BY=20
    BYTE=21
    CASE=22
    CATCH=23
    CHAR=24
    CHECKED=25
    CLASS=26
    CONST=27
    CONTINUE=28
    DECIMAL=29
    DEFAULT=30
    DELEGATE=31
    DESCENDING=32
    DO=33
    DOUBLE=34
    DYNAMIC=35
    ELSE=36
    ENUM=37
    EQUALS=38
    EVENT=39
    EXPLICIT=40
    EXTERN=41
    FALSE=42
    FINALLY=43
    FIXED=44
    FLOAT=45
    FOR=46
    FOREACH=47
    FROM=48
    GET=49
    GOTO=50
    GROUP=51
    IF=52
    IMPLICIT=53
    IN=54
    INT=55
    INTERFACE=56
    INTERNAL=57
    INTO=58
    IS=59
    JOIN=60
    LET=61
    LOCK=62
    LONG=63
    NAMEOF=64
    NAMESPACE=65
    NEW=66
    NULL_=67
    OBJECT=68
    ON=69
    OPERATOR=70
    ORDERBY=71
    OUT=72
    OVERRIDE=73
    PARAMS=74
    PARTIAL=75
    PRIVATE=76
    PROTECTED=77
    PUBLIC=78
    READONLY=79
    REF=80
    REMOVE=81
    RETURN=82
    SBYTE=83
    SEALED=84
    SELECT=85
    SET=86
    SHORT=87
    SIZEOF=88
    STACKALLOC=89
    STATIC=90
    STRING=91
    STRUCT=92
    SWITCH=93
    THIS=94
    THROW=95
    TRUE=96
    TRY=97
    TYPEOF=98
    UINT=99
    ULONG=100
    UNCHECKED=101
    UNMANAGED=102
    UNSAFE=103
    USHORT=104
    USING=105
    VAR=106
    VIRTUAL=107
    VOID=108
    VOLATILE=109
    WHEN=110
    WHERE=111
    WHILE=112
    YIELD=113
    IDENTIFIER=114
    LITERAL_ACCESS=115
    INTEGER_LITERAL=116
    HEX_INTEGER_LITERAL=117
    BIN_INTEGER_LITERAL=118
    REAL_LITERAL=119
    CHARACTER_LITERAL=120
    REGULAR_STRING=121
    VERBATIUM_STRING=122
    INTERPOLATED_REGULAR_STRING_START=123
    INTERPOLATED_VERBATIUM_STRING_START=124
    OPEN_BRACE=125
    CLOSE_BRACE=126
    OPEN_BRACKET=127
    CLOSE_BRACKET=128
    OPEN_PARENS=129
    CLOSE_PARENS=130
    DOT=131
    COMMA=132
    COLON=133
    SEMICOLON=134
    PLUS=135
    MINUS=136
    STAR=137
    DIV=138
    PERCENT=139
    AMP=140
    BITWISE_OR=141
    CARET=142
    BANG=143
    TILDE=144
    ASSIGNMENT=145
    LT=146
    GT=147
    INTERR=148
    DOUBLE_COLON=149
    OP_COALESCING=150
    OP_INC=151
    OP_DEC=152
    OP_AND=153
    OP_OR=154
    OP_PTR=155
    OP_EQ=156
    OP_NE=157
    OP_LE=158
    OP_GE=159
    OP_ADD_ASSIGNMENT=160
    OP_SUB_ASSIGNMENT=161
    OP_MULT_ASSIGNMENT=162
    OP_DIV_ASSIGNMENT=163
    OP_MOD_ASSIGNMENT=164
    OP_AND_ASSIGNMENT=165
    OP_OR_ASSIGNMENT=166
    OP_XOR_ASSIGNMENT=167
    OP_LEFT_SHIFT=168
    OP_LEFT_SHIFT_ASSIGNMENT=169
    OP_COALESCING_ASSIGNMENT=170
    OP_RANGE=171
    DOUBLE_CURLY_INSIDE=172
    OPEN_BRACE_INSIDE=173
    REGULAR_CHAR_INSIDE=174
    VERBATIUM_DOUBLE_QUOTE_INSIDE=175
    DOUBLE_QUOTE_INSIDE=176
    REGULAR_STRING_INSIDE=177
    VERBATIUM_INSIDE_STRING=178
    CLOSE_BRACE_INSIDE=179
    FORMAT_STRING=180
    DIRECTIVE_WHITESPACES=181
    DIGITS=182
    DEFINE=183
    UNDEF=184
    ELIF=185
    ENDIF=186
    LINE=187
    ERROR=188
    WARNING=189
    REGION=190
    ENDREGION=191
    PRAGMA=192
    NULLABLE=193
    DIRECTIVE_HIDDEN=194
    CONDITIONAL_SYMBOL=195
    DIRECTIVE_NEW_LINE=196
    TEXT=197
    DOUBLE_CURLY_CLOSE_INSIDE=198

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.9.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None


    Stack<Boolean> conditions = new Stack<Boolean>() {{ conditions.push(true); }};
    public HashSet<String> ConditionalSymbols = new HashSet<String>() {{ ConditionalSymbols.add("DEBUG"); }};

    private boolean allConditions() {
    	for(boolean condition: conditions) {
    		if (!condition)
    			return false;
    	}
    	return true;
    }



    class Preprocessor_directiveContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None


        def getRuleIndex(self):
            return CSharpPreprocessorParser.RULE_preprocessor_directive

     
        def copyFrom(self, ctx:ParserRuleContext):
            super().copyFrom(ctx)
            self.value = ctx.value



    class PreprocessorDiagnosticContext(Preprocessor_directiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSharpPreprocessorParser.Preprocessor_directiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def ERROR(self):
            return self.getToken(CSharpPreprocessorParser.ERROR, 0)
        def TEXT(self):
            return self.getToken(CSharpPreprocessorParser.TEXT, 0)
        def directive_new_line_or_sharp(self):
            return self.getTypedRuleContext(CSharpPreprocessorParser.Directive_new_line_or_sharpContext,0)

        def WARNING(self):
            return self.getToken(CSharpPreprocessorParser.WARNING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreprocessorDiagnostic" ):
                listener.enterPreprocessorDiagnostic(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreprocessorDiagnostic" ):
                listener.exitPreprocessorDiagnostic(self)


    class PreprocessorNullableContext(Preprocessor_directiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSharpPreprocessorParser.Preprocessor_directiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def NULLABLE(self):
            return self.getToken(CSharpPreprocessorParser.NULLABLE, 0)
        def TEXT(self):
            return self.getToken(CSharpPreprocessorParser.TEXT, 0)
        def directive_new_line_or_sharp(self):
            return self.getTypedRuleContext(CSharpPreprocessorParser.Directive_new_line_or_sharpContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreprocessorNullable" ):
                listener.enterPreprocessorNullable(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreprocessorNullable" ):
                listener.exitPreprocessorNullable(self)


    class PreprocessorRegionContext(Preprocessor_directiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSharpPreprocessorParser.Preprocessor_directiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def REGION(self):
            return self.getToken(CSharpPreprocessorParser.REGION, 0)
        def directive_new_line_or_sharp(self):
            return self.getTypedRuleContext(CSharpPreprocessorParser.Directive_new_line_or_sharpContext,0)

        def TEXT(self):
            return self.getToken(CSharpPreprocessorParser.TEXT, 0)
        def ENDREGION(self):
            return self.getToken(CSharpPreprocessorParser.ENDREGION, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreprocessorRegion" ):
                listener.enterPreprocessorRegion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreprocessorRegion" ):
                listener.exitPreprocessorRegion(self)


    class PreprocessorDeclarationContext(Preprocessor_directiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSharpPreprocessorParser.Preprocessor_directiveContext
            super().__init__(parser)
            self._CONDITIONAL_SYMBOL = None # Token
            self.copyFrom(ctx)

        def DEFINE(self):
            return self.getToken(CSharpPreprocessorParser.DEFINE, 0)
        def CONDITIONAL_SYMBOL(self):
            return self.getToken(CSharpPreprocessorParser.CONDITIONAL_SYMBOL, 0)
        def directive_new_line_or_sharp(self):
            return self.getTypedRuleContext(CSharpPreprocessorParser.Directive_new_line_or_sharpContext,0)

        def UNDEF(self):
            return self.getToken(CSharpPreprocessorParser.UNDEF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreprocessorDeclaration" ):
                listener.enterPreprocessorDeclaration(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreprocessorDeclaration" ):
                listener.exitPreprocessorDeclaration(self)


    class PreprocessorConditionalContext(Preprocessor_directiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSharpPreprocessorParser.Preprocessor_directiveContext
            super().__init__(parser)
            self.expr = None # Preprocessor_expressionContext
            self.copyFrom(ctx)

        def IF(self):
            return self.getToken(CSharpPreprocessorParser.IF, 0)
        def directive_new_line_or_sharp(self):
            return self.getTypedRuleContext(CSharpPreprocessorParser.Directive_new_line_or_sharpContext,0)

        def preprocessor_expression(self):
            return self.getTypedRuleContext(CSharpPreprocessorParser.Preprocessor_expressionContext,0)

        def ELIF(self):
            return self.getToken(CSharpPreprocessorParser.ELIF, 0)
        def ELSE(self):
            return self.getToken(CSharpPreprocessorParser.ELSE, 0)
        def ENDIF(self):
            return self.getToken(CSharpPreprocessorParser.ENDIF, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreprocessorConditional" ):
                listener.enterPreprocessorConditional(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreprocessorConditional" ):
                listener.exitPreprocessorConditional(self)


    class PreprocessorPragmaContext(Preprocessor_directiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSharpPreprocessorParser.Preprocessor_directiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def PRAGMA(self):
            return self.getToken(CSharpPreprocessorParser.PRAGMA, 0)
        def TEXT(self):
            return self.getToken(CSharpPreprocessorParser.TEXT, 0)
        def directive_new_line_or_sharp(self):
            return self.getTypedRuleContext(CSharpPreprocessorParser.Directive_new_line_or_sharpContext,0)


        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreprocessorPragma" ):
                listener.enterPreprocessorPragma(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreprocessorPragma" ):
                listener.exitPreprocessorPragma(self)


    class PreprocessorLineContext(Preprocessor_directiveContext):

        def __init__(self, parser, ctx:ParserRuleContext): # actually a CSharpPreprocessorParser.Preprocessor_directiveContext
            super().__init__(parser)
            self.copyFrom(ctx)

        def LINE(self):
            return self.getToken(CSharpPreprocessorParser.LINE, 0)
        def directive_new_line_or_sharp(self):
            return self.getTypedRuleContext(CSharpPreprocessorParser.Directive_new_line_or_sharpContext,0)

        def DIGITS(self):
            return self.getToken(CSharpPreprocessorParser.DIGITS, 0)
        def DEFAULT(self):
            return self.getToken(CSharpPreprocessorParser.DEFAULT, 0)
        def DIRECTIVE_HIDDEN(self):
            return self.getToken(CSharpPreprocessorParser.DIRECTIVE_HIDDEN, 0)
        def STRING(self):
            return self.getToken(CSharpPreprocessorParser.STRING, 0)

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreprocessorLine" ):
                listener.enterPreprocessorLine(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreprocessorLine" ):
                listener.exitPreprocessorLine(self)



    def preprocessor_directive(self):

        localctx = CSharpPreprocessorParser.Preprocessor_directiveContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_preprocessor_directive)
        self._la = 0 # Token type
        try:
            self.state = 80
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CSharpPreprocessorParser.DEFINE]:
                localctx = CSharpPreprocessorParser.PreprocessorDeclarationContext(self, localctx)
                self.enterOuterAlt(localctx, 1)
                self.state = 6
                self.match(CSharpPreprocessorParser.DEFINE)
                self.state = 7
                localctx._CONDITIONAL_SYMBOL = self.match(CSharpPreprocessorParser.CONDITIONAL_SYMBOL)
                self.state = 8
                self.directive_new_line_or_sharp()
                 ConditionalSymbols.add((None if localctx._CONDITIONAL_SYMBOL is None else localctx._CONDITIONAL_SYMBOL.text));
                	   localctx.value =  allConditions() 
                pass
            elif token in [CSharpPreprocessorParser.UNDEF]:
                localctx = CSharpPreprocessorParser.PreprocessorDeclarationContext(self, localctx)
                self.enterOuterAlt(localctx, 2)
                self.state = 11
                self.match(CSharpPreprocessorParser.UNDEF)
                self.state = 12
                localctx._CONDITIONAL_SYMBOL = self.match(CSharpPreprocessorParser.CONDITIONAL_SYMBOL)
                self.state = 13
                self.directive_new_line_or_sharp()
                 ConditionalSymbols.remove((None if localctx._CONDITIONAL_SYMBOL is None else localctx._CONDITIONAL_SYMBOL.text));
                	   localctx.value =  allConditions() 
                pass
            elif token in [CSharpPreprocessorParser.IF]:
                localctx = CSharpPreprocessorParser.PreprocessorConditionalContext(self, localctx)
                self.enterOuterAlt(localctx, 3)
                self.state = 16
                self.match(CSharpPreprocessorParser.IF)
                self.state = 17
                localctx.expr = self.preprocessor_expression(0)
                self.state = 18
                self.directive_new_line_or_sharp()
                 localctx.value =  localctx.expr.value.equals("true") && allConditions() conditions.push(localctx.expr.value.equals("true")); 
                pass
            elif token in [CSharpPreprocessorParser.ELIF]:
                localctx = CSharpPreprocessorParser.PreprocessorConditionalContext(self, localctx)
                self.enterOuterAlt(localctx, 4)
                self.state = 21
                self.match(CSharpPreprocessorParser.ELIF)
                self.state = 22
                localctx.expr = self.preprocessor_expression(0)
                self.state = 23
                self.directive_new_line_or_sharp()
                 if (!conditions.peek()) { conditions.pop(); localctx.value =  localctx.expr.value.equals("true") && allConditions()
                	     conditions.push(localctx.expr.value.equals("true")); } else localctx.value =  false 
                pass
            elif token in [CSharpPreprocessorParser.ELSE]:
                localctx = CSharpPreprocessorParser.PreprocessorConditionalContext(self, localctx)
                self.enterOuterAlt(localctx, 5)
                self.state = 26
                self.match(CSharpPreprocessorParser.ELSE)
                self.state = 27
                self.directive_new_line_or_sharp()
                 if (!conditions.peek()) { conditions.pop(); localctx.value =  true && allConditions() conditions.push(true); }
                	    else localctx.value =  false 
                pass
            elif token in [CSharpPreprocessorParser.ENDIF]:
                localctx = CSharpPreprocessorParser.PreprocessorConditionalContext(self, localctx)
                self.enterOuterAlt(localctx, 6)
                self.state = 30
                self.match(CSharpPreprocessorParser.ENDIF)
                self.state = 31
                self.directive_new_line_or_sharp()
                 conditions.pop(); localctx.value =  conditions.peek() 
                pass
            elif token in [CSharpPreprocessorParser.LINE]:
                localctx = CSharpPreprocessorParser.PreprocessorLineContext(self, localctx)
                self.enterOuterAlt(localctx, 7)
                self.state = 34
                self.match(CSharpPreprocessorParser.LINE)
                self.state = 41
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [CSharpPreprocessorParser.DIGITS]:
                    self.state = 35
                    self.match(CSharpPreprocessorParser.DIGITS)
                    self.state = 37
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)
                    if _la==CSharpPreprocessorParser.STRING:
                        self.state = 36
                        self.match(CSharpPreprocessorParser.STRING)


                    pass
                elif token in [CSharpPreprocessorParser.DEFAULT]:
                    self.state = 39
                    self.match(CSharpPreprocessorParser.DEFAULT)
                    pass
                elif token in [CSharpPreprocessorParser.DIRECTIVE_HIDDEN]:
                    self.state = 40
                    self.match(CSharpPreprocessorParser.DIRECTIVE_HIDDEN)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 43
                self.directive_new_line_or_sharp()
                 localctx.value =  allConditions() 
                pass
            elif token in [CSharpPreprocessorParser.ERROR]:
                localctx = CSharpPreprocessorParser.PreprocessorDiagnosticContext(self, localctx)
                self.enterOuterAlt(localctx, 8)
                self.state = 46
                self.match(CSharpPreprocessorParser.ERROR)
                self.state = 47
                self.match(CSharpPreprocessorParser.TEXT)
                self.state = 48
                self.directive_new_line_or_sharp()
                 localctx.value =  allConditions() 
                pass
            elif token in [CSharpPreprocessorParser.WARNING]:
                localctx = CSharpPreprocessorParser.PreprocessorDiagnosticContext(self, localctx)
                self.enterOuterAlt(localctx, 9)
                self.state = 51
                self.match(CSharpPreprocessorParser.WARNING)
                self.state = 52
                self.match(CSharpPreprocessorParser.TEXT)
                self.state = 53
                self.directive_new_line_or_sharp()
                 localctx.value =  allConditions() 
                pass
            elif token in [CSharpPreprocessorParser.REGION]:
                localctx = CSharpPreprocessorParser.PreprocessorRegionContext(self, localctx)
                self.enterOuterAlt(localctx, 10)
                self.state = 56
                self.match(CSharpPreprocessorParser.REGION)
                self.state = 58
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CSharpPreprocessorParser.TEXT:
                    self.state = 57
                    self.match(CSharpPreprocessorParser.TEXT)


                self.state = 60
                self.directive_new_line_or_sharp()
                 localctx.value =  allConditions() 
                pass
            elif token in [CSharpPreprocessorParser.ENDREGION]:
                localctx = CSharpPreprocessorParser.PreprocessorRegionContext(self, localctx)
                self.enterOuterAlt(localctx, 11)
                self.state = 63
                self.match(CSharpPreprocessorParser.ENDREGION)
                self.state = 65
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if _la==CSharpPreprocessorParser.TEXT:
                    self.state = 64
                    self.match(CSharpPreprocessorParser.TEXT)


                self.state = 67
                self.directive_new_line_or_sharp()
                 localctx.value =  allConditions() 
                pass
            elif token in [CSharpPreprocessorParser.PRAGMA]:
                localctx = CSharpPreprocessorParser.PreprocessorPragmaContext(self, localctx)
                self.enterOuterAlt(localctx, 12)
                self.state = 70
                self.match(CSharpPreprocessorParser.PRAGMA)
                self.state = 71
                self.match(CSharpPreprocessorParser.TEXT)
                self.state = 72
                self.directive_new_line_or_sharp()
                 localctx.value =  allConditions() 
                pass
            elif token in [CSharpPreprocessorParser.NULLABLE]:
                localctx = CSharpPreprocessorParser.PreprocessorNullableContext(self, localctx)
                self.enterOuterAlt(localctx, 13)
                self.state = 75
                self.match(CSharpPreprocessorParser.NULLABLE)
                self.state = 76
                self.match(CSharpPreprocessorParser.TEXT)
                self.state = 77
                self.directive_new_line_or_sharp()
                 localctx.value =  allConditions() 
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Directive_new_line_or_sharpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DIRECTIVE_NEW_LINE(self):
            return self.getToken(CSharpPreprocessorParser.DIRECTIVE_NEW_LINE, 0)

        def EOF(self):
            return self.getToken(CSharpPreprocessorParser.EOF, 0)

        def getRuleIndex(self):
            return CSharpPreprocessorParser.RULE_directive_new_line_or_sharp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDirective_new_line_or_sharp" ):
                listener.enterDirective_new_line_or_sharp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDirective_new_line_or_sharp" ):
                listener.exitDirective_new_line_or_sharp(self)




    def directive_new_line_or_sharp(self):

        localctx = CSharpPreprocessorParser.Directive_new_line_or_sharpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_directive_new_line_or_sharp)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            _la = self._input.LA(1)
            if not(_la==CSharpPreprocessorParser.EOF or _la==CSharpPreprocessorParser.DIRECTIVE_NEW_LINE):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Preprocessor_expressionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser
            self.value = None
            self.expr1 = None # Preprocessor_expressionContext
            self._CONDITIONAL_SYMBOL = None # Token
            self.expr = None # Preprocessor_expressionContext
            self.expr2 = None # Preprocessor_expressionContext

        def TRUE(self):
            return self.getToken(CSharpPreprocessorParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(CSharpPreprocessorParser.FALSE, 0)

        def CONDITIONAL_SYMBOL(self):
            return self.getToken(CSharpPreprocessorParser.CONDITIONAL_SYMBOL, 0)

        def OPEN_PARENS(self):
            return self.getToken(CSharpPreprocessorParser.OPEN_PARENS, 0)

        def CLOSE_PARENS(self):
            return self.getToken(CSharpPreprocessorParser.CLOSE_PARENS, 0)

        def preprocessor_expression(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(CSharpPreprocessorParser.Preprocessor_expressionContext)
            else:
                return self.getTypedRuleContext(CSharpPreprocessorParser.Preprocessor_expressionContext,i)


        def BANG(self):
            return self.getToken(CSharpPreprocessorParser.BANG, 0)

        def OP_EQ(self):
            return self.getToken(CSharpPreprocessorParser.OP_EQ, 0)

        def OP_NE(self):
            return self.getToken(CSharpPreprocessorParser.OP_NE, 0)

        def OP_AND(self):
            return self.getToken(CSharpPreprocessorParser.OP_AND, 0)

        def OP_OR(self):
            return self.getToken(CSharpPreprocessorParser.OP_OR, 0)

        def getRuleIndex(self):
            return CSharpPreprocessorParser.RULE_preprocessor_expression

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPreprocessor_expression" ):
                listener.enterPreprocessor_expression(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPreprocessor_expression" ):
                listener.exitPreprocessor_expression(self)



    def preprocessor_expression(self, _p:int=0):
        _parentctx = self._ctx
        _parentState = self.state
        localctx = CSharpPreprocessorParser.Preprocessor_expressionContext(self, self._ctx, _parentState)
        _prevctx = localctx
        _startState = 4
        self.enterRecursionRule(localctx, 4, self.RULE_preprocessor_expression, _p)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 100
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [CSharpPreprocessorParser.TRUE]:
                self.state = 85
                self.match(CSharpPreprocessorParser.TRUE)
                 localctx.value =  "true" 
                pass
            elif token in [CSharpPreprocessorParser.FALSE]:
                self.state = 87
                self.match(CSharpPreprocessorParser.FALSE)
                 localctx.value =  "false" 
                pass
            elif token in [CSharpPreprocessorParser.CONDITIONAL_SYMBOL]:
                self.state = 89
                localctx._CONDITIONAL_SYMBOL = self.match(CSharpPreprocessorParser.CONDITIONAL_SYMBOL)
                 localctx.value =  ConditionalSymbols.contains((None if localctx._CONDITIONAL_SYMBOL is None else localctx._CONDITIONAL_SYMBOL.text)) ? "true" : "false" 
                pass
            elif token in [CSharpPreprocessorParser.OPEN_PARENS]:
                self.state = 91
                self.match(CSharpPreprocessorParser.OPEN_PARENS)
                self.state = 92
                localctx.expr = self.preprocessor_expression(0)
                self.state = 93
                self.match(CSharpPreprocessorParser.CLOSE_PARENS)
                 localctx.value =  localctx.expr.value 
                pass
            elif token in [CSharpPreprocessorParser.BANG]:
                self.state = 96
                self.match(CSharpPreprocessorParser.BANG)
                self.state = 97
                localctx.expr = self.preprocessor_expression(5)
                 localctx.value =  localctx.expr.value.equals("true") ? "false" : "true" 
                pass
            else:
                raise NoViableAltException(self)

            self._ctx.stop = self._input.LT(-1)
            self.state = 124
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,7,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    if self._parseListeners is not None:
                        self.triggerExitRuleEvent()
                    _prevctx = localctx
                    self.state = 122
                    self._errHandler.sync(self)
                    la_ = self._interp.adaptivePredict(self._input,6,self._ctx)
                    if la_ == 1:
                        localctx = CSharpPreprocessorParser.Preprocessor_expressionContext(self, _parentctx, _parentState)
                        localctx.expr1 = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_preprocessor_expression)
                        self.state = 102
                        if not self.precpred(self._ctx, 4):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 4)")
                        self.state = 103
                        self.match(CSharpPreprocessorParser.OP_EQ)
                        self.state = 104
                        localctx.expr2 = self.preprocessor_expression(5)
                         localctx.value =  (localctx.expr1.value == localctx.expr2.value ? "true" : "false") 
                        pass

                    elif la_ == 2:
                        localctx = CSharpPreprocessorParser.Preprocessor_expressionContext(self, _parentctx, _parentState)
                        localctx.expr1 = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_preprocessor_expression)
                        self.state = 107
                        if not self.precpred(self._ctx, 3):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 3)")
                        self.state = 108
                        self.match(CSharpPreprocessorParser.OP_NE)
                        self.state = 109
                        localctx.expr2 = self.preprocessor_expression(4)
                         localctx.value =  (localctx.expr1.value != localctx.expr2.value ? "true" : "false") 
                        pass

                    elif la_ == 3:
                        localctx = CSharpPreprocessorParser.Preprocessor_expressionContext(self, _parentctx, _parentState)
                        localctx.expr1 = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_preprocessor_expression)
                        self.state = 112
                        if not self.precpred(self._ctx, 2):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 2)")
                        self.state = 113
                        self.match(CSharpPreprocessorParser.OP_AND)
                        self.state = 114
                        localctx.expr2 = self.preprocessor_expression(3)
                         localctx.value =  (localctx.expr1.value.equals("true") && localctx.expr2.value.equals("true") ? "true" : "false") 
                        pass

                    elif la_ == 4:
                        localctx = CSharpPreprocessorParser.Preprocessor_expressionContext(self, _parentctx, _parentState)
                        localctx.expr1 = _prevctx
                        self.pushNewRecursionContext(localctx, _startState, self.RULE_preprocessor_expression)
                        self.state = 117
                        if not self.precpred(self._ctx, 1):
                            from antlr4.error.Errors import FailedPredicateException
                            raise FailedPredicateException(self, "self.precpred(self._ctx, 1)")
                        self.state = 118
                        self.match(CSharpPreprocessorParser.OP_OR)
                        self.state = 119
                        localctx.expr2 = self.preprocessor_expression(2)
                         localctx.value =  (localctx.expr1.value.equals("true") || localctx.expr2.value.equals("true") ? "true" : "false") 
                        pass

             
                self.state = 126
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,7,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.unrollRecursionContexts(_parentctx)
        return localctx



    def sempred(self, localctx:RuleContext, ruleIndex:int, predIndex:int):
        if self._predicates == None:
            self._predicates = dict()
        self._predicates[2] = self.preprocessor_expression_sempred
        pred = self._predicates.get(ruleIndex, None)
        if pred is None:
            raise Exception("No predicate with index:" + str(ruleIndex))
        else:
            return pred(localctx, predIndex)

    def preprocessor_expression_sempred(self, localctx:Preprocessor_expressionContext, predIndex:int):
            if predIndex == 0:
                return self.precpred(self._ctx, 4)
         

            if predIndex == 1:
                return self.precpred(self._ctx, 3)
         

            if predIndex == 2:
                return self.precpred(self._ctx, 2)
         

            if predIndex == 3:
                return self.precpred(self._ctx, 1)
         




