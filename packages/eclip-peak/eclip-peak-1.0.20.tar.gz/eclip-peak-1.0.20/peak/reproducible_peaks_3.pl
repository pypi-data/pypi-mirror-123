#!/usr/bin/env perl

use warnings;
use strict;

my $hashing_value = 10000;
my $l2fc_cutoff = 3;
if (exists $ARGV[12]) {
    $l2fc_cutoff = $ARGV[12];
}

my $l10p_cutoff = 3;
if (exists $ARGV[13]) {
    $l10p_cutoff = $ARGV[13];
}

my $idr_cutoff = 0.01;
if (exists $ARGV[14]) {
    $idr_cutoff = $ARGV[14];
}

my %idr_cutoffs = ("0.001" => "1000", "0.005" => "955", "0.01" => "830", "0.02" => "705", "0.03" => "632",
    "0.04" => "580", "0.05" => "540", "0.06" => "507", "0.07" => "479", "0.08" => "455", "0.09" => "434",
    "0.1" => "415", "0.2" => "290", "0.3" => "217", "0.4" => "165", "0.5" => "125", "1" => "0");

my $rep1_idr_merged_full_bed = $ARGV[0];
my $rep2_idr_merged_full_bed = $ARGV[1];
my $rep3_idr_merged_full_bed = $ARGV[2];

my $rep1_full_out = $ARGV[3];
my $rep2_full_out = $ARGV[4];
my $rep3_full_out = $ARGV[5];
open(REP1FULL,">$rep1_full_out") || die "Cannot open $rep1_full_out for writing!\n";
print REP1FULL "# chrom\tstart\tstop\tpeak\tip_reads\tinput_reads\tp\tstatistic\tmethod\tstatus\tl10p\tl2fc\n";
open(REP2FULL,">$rep2_full_out") || die "Cannot open $rep2_full_out for writing!\n";
print REP2FULL "# chrom\tstart\tstop\tpeak\tip_reads\tinput_reads\tp\tstatistic\tmethod\tstatus\tl10p\tl2fc\n";
open(REP3FULL,">$rep3_full_out") || die "Cannot open $rep3_full_out for writing!\n";
print REP3FULL "# chrom\tstart\tstop\tpeak\tip_reads\tinput_reads\tp\tstatistic\tmethod\tstatus\tl10p\tl2fc\n";

my $bed_output = $ARGV[6];
my $custom_bed_output = $ARGV[7];
open(BEDOUT,">$bed_output") || die "Cannot open $bed_output for writing!\n";
open(CUSTOMOUT,">$custom_bed_output") || die "Cannot open $custom_bed_output for writing!\n";
print CUSTOMOUT "# idr_region\tpeak\tgeo_mean\tl2fc_1\tl2fc_2\tl2fc_3\tl10p_1\tl10p_2\tl10p_3\n";

my $file1 = $ARGV[8];
my $file2 = $ARGV[9];
my $file3 = $ARGV[10];

my $idr_file = $ARGV[11];
my %idr_output;
&parse_idr_file($idr_file);

my %idrregion2peaks;
&parse_file($file1);
&parse_file($file2);
&parse_file($file3);
my %peak_info;

&parse_input_norm_full_file($rep1_idr_merged_full_bed);
&parse_input_norm_full_file($rep2_idr_merged_full_bed);
&parse_input_norm_full_file($rep3_idr_merged_full_bed);


my $count_signif=0;
my %idrregion2maxgeommean;
for my $idrregion (keys %idrregion2peaks) {
    my %peak_geommean;
    my %peak_len;
    my %peak_start;
    my %peak_stop;
    for my $peak (keys %{$idrregion2peaks{$idrregion}}) {
        #	print STDERR "peak $peak rep1_idr_merged_full_bed $rep1_idr_merged_full_bed rep2_idr_merged_full_bed $rep2_idr_merged_full_bed rep3_idr_merged_full_bed $rep3_idr_merged_full_bed\n";
        my $geometric_mean = log(( (2 ** $peak_info{$peak}{$rep1_idr_merged_full_bed}{l2fc}) *
            (2 ** $peak_info{$peak}{$rep2_idr_merged_full_bed}{l2fc}) *
            (2 ** $peak_info{$peak}{$rep3_idr_merged_full_bed}{l2fc}))**(1/3))/log(2);
        unless ($geometric_mean) {
        #	    print STDERR "peak $peak rep1_idr_merged_full_bed $rep1_idr_merged_full_bed rep2_idr_merged_full_bed $rep2_idr_merged_full_bed rep3_idr_merged_full_bed $rep3_idr_merged_full_bed\n";
        #	    print STDERR "rep1 ".$peak_info{$peak}{$rep1_idr_merged_full_bed}{l2fc}." rep2 ".$peak_info{$peak}{$rep2_idr_merged_full_bed}{l2fc}." rep3 ".$peak_info{$peak}{$rep3_idr_merged_full_bed}{l2fc}."\n";
        }
        $peak_geommean{$peak} = sprintf("%.7f",$geometric_mean);

        my ($chr,$pos,$str) = split(/\:/,$peak);
        my ($start,$stop) = split(/\-/,$pos);
        $peak_len{$peak} = $stop - $start;
        $peak_start{$peak} = $start;
        $peak_stop{$peak} = $stop;
    }
    my @sorted_peak_geommeans = sort {$peak_geommean{$b} <=> $peak_geommean{$a} ||
        $peak_len{$b} <=> $peak_len{$a} ||
        $peak_start{$b} <=> $peak_start{$a} ||
        $peak_stop{$b} <=> $peak_stop{$a}} keys %peak_geommean;
    #    my @sorted_peak_geommeans = sort {$peak_geommean{$b} <=> $peak_geommean{$a}} keys %peak_geommean;
    $idrregion2maxgeommean{$idrregion}{geom} = $peak_geommean{$sorted_peak_geommeans[0]};

    my ($idrreg_chr,$idrreg_pos,$idrreg_str,$idrreg_val) = split(/\:/,$idrregion);
    my ($idrreg_start,$idrreg_stop) = split(/\-/,$idrreg_pos);
    $idrregion2maxgeommean{$idrregion}{len} = $idrreg_stop - $idrreg_start;
    $idrregion2maxgeommean{$idrregion}{start} = $idrreg_start;
    $idrregion2maxgeommean{$idrregion}{stop} = $idrreg_stop;
}

my %already_used_peaks;
my @already_used_peaks_array;

my @sorted_idrregions = sort {$idrregion2maxgeommean{$b}{geom} <=> $idrregion2maxgeommean{$a}{geom} ||
				  $idrregion2maxgeommean{$b}{len} <=> $idrregion2maxgeommean{$a}{len} ||
				  $idrregion2maxgeommean{$a}{start} <=> $idrregion2maxgeommean{$b}{start} ||
				  $idrregion2maxgeommean{$a}{stop} <=> $idrregion2maxgeommean{$b}{stop}} keys %idrregion2maxgeommean;
for my $idrregion (@sorted_idrregions) {
    my %peak_geommean;
    my %peak_len;
    my %peak_start;
    my %peak_stop;
    for my $peak (keys %{$idrregion2peaks{$idrregion}}) {
        my $geometric_mean = log(( (2 ** $peak_info{$peak}{$rep1_idr_merged_full_bed}{l2fc}) *
            (2 ** $peak_info{$peak}{$rep2_idr_merged_full_bed}{l2fc}) *
            (2 ** $peak_info{$peak}{$rep3_idr_merged_full_bed}{l2fc}) ) ** (1/3))/log(2);
        $peak_geommean{$peak} = sprintf("%.7f",$geometric_mean);
        my ($chr,$pos,$str) = split(/\:/,$peak);
        my ($start,$stop) = split(/\-/,$pos);
        $peak_len{$peak} = $stop - $start;
        $peak_start{$peak} = $start;
        $peak_stop{$peak} = $stop;
    }

    my @peaks_sorted = sort {$peak_geommean{$b} <=> $peak_geommean{$a} ||
				 $peak_len{$b} <=> $peak_len{$a} ||
				 $peak_start{$a} <=> $peak_start{$b} ||
				 $peak_stop{$a} <=> $peak_stop{$b}} keys %peak_geommean;
    
#    print BEDOUT "IDR region $idrregion geom $idrregion2maxgeommean{$idrregion}{geom} len $idrregion2maxgeommean{$idrregion}{len} start $idrregion2maxgeommean{$idrregion}{start} stop $idrregion2maxgeommean{$idrregion}{stop}\n";

    for my $peak (@peaks_sorted) {
        #first check if overlaps existing 
	next if (exists $already_used_peaks{$peak});
        my ($chr,$pos,$str) = split(/\:/,$peak);
        my ($start,$stop) = split(/\-/,$pos);
	
	my $flag = 0;

	for my $peak2 (@already_used_peaks_array) {
	    my ($chr2,$pos2,$str2) = split(/\:/,$peak2);
	    my ($start2,$stop2) = split(/\-/,$pos2);

            next if ($start2 >= $stop);
            next if ($start >= $stop2);
            $flag = 1;
        }
        next if ($flag == 1);

        # ok doesn't overlap existing
        #first time through - only check significant peaks

        next unless ($peak_info{$peak}{$rep1_idr_merged_full_bed}{l10p} >= $l10p_cutoff &&
            $peak_info{$peak}{$rep2_idr_merged_full_bed}{l10p} >= $l10p_cutoff &&
            $peak_info{$peak}{$rep3_idr_merged_full_bed}{l10p} >= $l10p_cutoff);

        $already_used_peaks{$peak} = 1;
	push @already_used_peaks_array,$peak;

        print CUSTOMOUT "".$idrregion."\t".$peak."\t".$peak_geommean{$peak}."\t".
            $peak_info{$peak}{$rep1_idr_merged_full_bed}{l2fc}."\t".
            $peak_info{$peak}{$rep2_idr_merged_full_bed}{l2fc}."\t".
            $peak_info{$peak}{$rep3_idr_merged_full_bed}{l2fc}."\t".
            $peak_info{$peak}{$rep1_idr_merged_full_bed}{l10p}."\t".
            $peak_info{$peak}{$rep2_idr_merged_full_bed}{l10p}."\t".
            $peak_info{$peak}{$rep3_idr_merged_full_bed}{l10p}."\n";

	    if ($peak_geommean{$peak} >= $l2fc_cutoff &&
            $peak_info{$peak}{$rep1_idr_merged_full_bed}{l10p} >= $l10p_cutoff &&
            $peak_info{$peak}{$rep2_idr_merged_full_bed}{l10p} >= $l10p_cutoff &&
            $peak_info{$peak}{$rep3_idr_merged_full_bed}{l10p} >= $l10p_cutoff) {
            print BEDOUT "".$chr."\t".$start."\t".$stop."\t".
                &min($peak_info{$peak}{$rep1_idr_merged_full_bed}{l10p},
                    $peak_info{$peak}{$rep2_idr_merged_full_bed}{l10p},
                    $peak_info{$peak}{$rep3_idr_merged_full_bed}{l10p}).
                "\t".$peak_geommean{$peak}."\t".$str."\n";
	}

        my @rep1_full = split(/\t/,$peak_info{$peak}{$rep1_idr_merged_full_bed}{full});
        $rep1_full[3] .= ":".$peak_geommean{$peak};
        my $rep1_full_join = join("\t",@rep1_full);
        print REP1FULL "".$rep1_full_join."\n";

        my @rep2_full = split(/\t/,$peak_info{$peak}{$rep2_idr_merged_full_bed}{full});
        $rep2_full[3] .= ":".$peak_geommean{$peak};
        my $rep2_full_join = join("\t",@rep2_full);
        print REP2FULL "".$rep2_full_join."\n";

        my @rep3_full = split(/\t/,$peak_info{$peak}{$rep3_idr_merged_full_bed}{full});
        $rep3_full[3] .= ":".$peak_geommean{$peak};
        my $rep3_full_join = join("\t",@rep3_full);
        print REP3FULL "".$rep3_full_join."\n";

        $count_signif++ if ($peak_geommean{$peak} >= 3);
    }
    for my $peak (@peaks_sorted) {
        #first check if overlaps existing
	next if (exists $already_used_peaks{$peak});
	
        my ($chr,$pos,$str) = split(/\:/,$peak);
        my ($start,$stop) = split(/\-/,$pos);

        my $flag = 0;
        next if (exists $already_used_peaks{$peak});
	
        for my $peak2 (@already_used_peaks_array) {
            my ($chr2,$pos2,$str2) = split(/\:/,$peak2);
            my ($start2,$stop2) = split(/\-/,$pos2);
	    
            next if ($start2 >=$stop);
            next if ($start >= $stop2);
            $flag = 1;
        }
        next if ($flag == 1);
	
        # ok doesn't overlap existing

        #second time through - check all genes
        $already_used_peaks{$peak} = 1;
	push @already_used_peaks_array,$peak;

        print CUSTOMOUT "".$idrregion."\t".$peak."\t".$peak_geommean{$peak}."\t".
            $peak_info{$peak}{$rep1_idr_merged_full_bed}{l2fc}."\t".
            $peak_info{$peak}{$rep2_idr_merged_full_bed}{l2fc}."\t".
            $peak_info{$peak}{$rep3_idr_merged_full_bed}{l2fc}."\t".
            $peak_info{$peak}{$rep1_idr_merged_full_bed}{l10p}."\t".
            $peak_info{$peak}{$rep2_idr_merged_full_bed}{l10p}."\t".
            $peak_info{$peak}{$rep3_idr_merged_full_bed}{l10p}."\n";

        if ($peak_geommean{$peak} >= $l2fc_cutoff &&
            $peak_info{$peak}{$rep1_idr_merged_full_bed}{l10p} >= $l10p_cutoff &&
            $peak_info{$peak}{$rep2_idr_merged_full_bed}{l10p} >= $l10p_cutoff &&
            $peak_info{$peak}{$rep3_idr_merged_full_bed}{l10p} >= $l10p_cutoff) {
            print BEDOUT "".$chr."\t".$start."\t".$stop."\t".
                &min($peak_info{$peak}{$rep1_idr_merged_full_bed}{l10p},
                    $peak_info{$peak}{$rep2_idr_merged_full_bed}{l10p},
                    $peak_info{$peak}{$rep3_idr_merged_full_bed}{l10p})."\t".
                $peak_geommean{$peak}."\t".$str."\n";

        }

        my @rep1_full = split(/\t/,$peak_info{$peak}{$rep1_idr_merged_full_bed}{full});
        $rep1_full[3] .= ":".$peak_geommean{$peak};
        my $rep1_full_join = join("\t",@rep1_full);
        print REP1FULL "".$rep1_full_join."\n";

        my @rep2_full = split(/\t/,$peak_info{$peak}{$rep2_idr_merged_full_bed}{full});
        $rep2_full[3] .= ":".$peak_geommean{$peak};
        my $rep2_full_join = join("\t",@rep2_full);
        print REP2FULL "".$rep2_full_join."\n";

        my @rep3_full = split(/\t/,$peak_info{$peak}{$rep3_idr_merged_full_bed}{full});
        $rep3_full[3] .= ":".$peak_geommean{$peak};
        my $rep3_full_join = join("\t",@rep3_full);
        print REP3FULL "".$rep3_full_join."\n";
    }
}

print STDERR "IDR and geommean(fc) >= 3 && p-value >= 3 in both reps: $count_signif\n";
close(REP1FULL);
close(REP2FULL);
close(REP3FULL);
close(CUSTOMOUT);
close(BEDOUT);


sub parse_input_norm_full_file {
    my $input_norm_file = shift;
    print STDERR "Parsing $input_norm_file\n";
    open(INF,$input_norm_file) || die "Cannot open $input_norm_file for reading!\n";
    for my $line (<INF>) {
        chomp($line);
        next if ($line =~ /^\#/);
        my @tmp = split(/\t/,$line);
        my $chr = $tmp[0];
        my $start = $tmp[1];
        my $stop = $tmp[2];
        my ($chr2,$pos2,$str,$del) = split(/\:/,$tmp[3]);
        $tmp[3] = $chr2.":".$pos2.":".$str;
        my $l2fc = $tmp[11];
        my $l10p = $tmp[10];

#	if ($start eq "208601180") {
#	    print STDERR "line $line fi $input_norm_file\n";
#	}

        $peak_info{$chr.":".$start."-".$stop.":".$str}{$input_norm_file}{l2fc} = $l2fc;
        $peak_info{$chr.":".$start."-".$stop.":".$str}{$input_norm_file}{l10p} = $l10p;
        $peak_info{$chr.":".$start."-".$stop.":".$str}{$input_norm_file}{full} = join("\t",@tmp);
    }
    close(INF);

}

sub parse_file {
    my $file = shift;
    print STDERR "Parsing $file ...\n";
    open(F,$file) || die "Cannot open $file for reading!\n";
    for my $line (<F>) {
        chomp($line);
        next if ($line =~ /^\#/);
        my @tmp = split(/\t/,$line);
        my $chr = $tmp[0];
        my $start = $tmp[1];
        my $stop = $tmp[2];
        #	if ($start eq "208601180") {
        #           print STDERR "line $line fi $file\n";
        #	}
        my ($chr2,$pos2,$str,$p) = split(/\:/,$tmp[3]);
        my $entropy = $tmp[15];
        my $l2fc = $tmp[11];
        my $l10p = $tmp[10];

        next unless ($l2fc >= $l2fc_cutoff && $l10p >= $l10p_cutoff);

        my $x = int($start / $hashing_value);
        my $y = int($stop / $hashing_value);

        my %overlapping_idrs;

        for my $i ($x..$y) {
            for my $idr_peak (@{$idr_output{$chr}{$str}{$i}}) {
                my ($ichr,$ipos,$istr,$iidr) = split(/\:/,$idr_peak);
                my ($istart,$istop) = split(/\-/,$ipos);
                next if ($istart >= $stop);
                next if ($istop <= $start);
                $overlapping_idrs{$idr_peak} = $iidr;
            }
        }
	
        if (scalar(keys %overlapping_idrs) > 0) {

            # if (scalar(keys %overlapping_idrs) > 1) {
            #     print STDERR "This should NEVER be hit - peak overlaps with more than one IDR region $line\n".join("\t",keys %overlapping_idrs)."\n---\n";
            # }

            for my $overlapping_idrpeak (keys %overlapping_idrs) {
                my ($ichr,$ipos,$istr,$iidr) = split(/\:/,$overlapping_idrpeak);
                if ($iidr >= $idr_cutoffs{$idr_cutoff}) {
                    $idrregion2peaks{$overlapping_idrpeak}{$chr.":".$start."-".$stop.":".$str} = 1;
                }
            }
        } else {
            # peak not in IDR list
        }
    }
    close(F);
}

sub parse_idr_file {
    my $idr_file = shift;
    print STDERR "Parsing $idr_file ...\n";
    open(ID,$idr_file) || die "Cannot open $idr_file for reading!\n";
    for my $line (<ID>) {
        chomp($line);
        next if ($line =~ /^\#/);
        my @tmp = split(/\t/,$line);
        my $chr = $tmp[0];
        my $start = $tmp[1];
        my $stop = $tmp[2];
        my $str = $tmp[5];
        my $x = int($start / $hashing_value);
        my $y = int($stop / $hashing_value);

        for my $i ($x..$y) {
            push @{$idr_output{$chr}{$str}{$i}},$chr.":".$start."-".$stop.":".$str.":"."1000";
            }
        }
    close(ID);
}


sub min {
    my $x = shift;
    my $y = shift;
    my $z = shift;

    my @array = ($x,$y,$z);
    my @sorted = sort {$a <=> $b} @array;
    return($sorted[0]);

}
