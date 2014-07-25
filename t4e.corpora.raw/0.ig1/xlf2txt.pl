#!/usr/bin/perl 

#Converts XLIFF format into plain text
#Copyright Marcello Federico, FBK, April 2013

use strict;
use Getopt::Long "GetOptions";

my ($help,$txt,$xlf,$strip,$debug)=();
$txt="";
$xlf="";


$help=1 unless

&GetOptions(
        'txt=s' => \$txt,
        'xlf=s' =>  \$xlf,
        'strip' =>  \$strip,
        'help' =>   \$help);

if ($help){
  print "xlf2txt.pl <options>\n",
  "--txt <file>  text file (default stdout) \n",
  "--xlf <file>  xliff file (file stdin)\n",
  "--strip       strip source from input (default false)\n",
  "--help        print these instructions\n";    
  exit(1);
}


########################################

open(XLF,($xlf?" < $xlf":"cat|")) || die "Cannot open XLF file $xlf\n";
open(TXT,($txt?"> $txt":"|cat")) || die "Cannot open txt file $txt\n";

while (<XLF>){
    if (/\<question_text>(.*)\<\/question_text></ && !$strip){
       print $1,"\n";
    };
   }
