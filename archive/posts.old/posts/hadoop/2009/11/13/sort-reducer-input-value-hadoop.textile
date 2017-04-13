I HIGHLY recommend that you read the email thread by "Owen O'Malley":http://markmail.org/message/7gonm3kiasyh2xnf#query:setOutputKeyComparatorClass+page:3+mid:esn3lgzyx3ag26cy+state:results that describes this technique in brief. I should also note that this example is using the 0.18 Hadoop API. 

h5. PROBLEM STATEMENT

Suppose we have a file with a bunch of comma/line separated letters:

bc. l,f,a,e,a,a,l
f,g,b,c,b,d,f
x,i,t,u,f,e,h
...etc

We want our reducer to receive bigrams (lf, fa, ae, ea, aa, al, etc), but partitioned by the first letter, and sorted (ascending) by the second. For example, for the letter a, the reducer should receive:

bc. <a, [l,e,a]>

This is actually somewhat difficult to do, since we want to partition by key, but sort the reducer's values iterator. The trick is to have the mapper output the bigram in the key, and only the second letter in the value. For the example above, the mapper would emit:

bc. <ae, e>
<aa, a>
<al, l>
...

We can then use a custom partitioner/sorter to partition and sort according to our needs. 

h5. SORTING BY VALUE

To sort Hadoop's mapper output by value, you need to set three settings in your JobConf:

* setPartitionerClass
* setOutputValueGroupingComparator
* setOutputKeyComparatorClass

There are many threads that say that you can't sort by value in Hadoop. This is true. What you can do, instead, is have your mapper output all data in the key, rather than the value. Then you can use a specialized Partitioner classes and two RawComparator classes to sort and partition your map output properly. 

h5. PARTITIONER

The first class that you need to set is a class that extends org.apache.hadoop.mapred.Partitioner. This class has a single function that determines which partition your map output should go to. This means that you can't go below 0, or above numPartitions - 1. Mostly, you'll want to hashCode() some portion of your key and mod it by numPartitions. 

In our example, the partitioner will partition by the first letter of the key. 

h5. OUTPUT VALUE GROUPING COMPARATOR

The OutputValueGroupingComparator JobConf setting takes in a org.apache.hadoop.io.RawComparator. This RawComparator is used to determine which reducer the mapper output row should go to. This RawComparator does not sort a reducer's value iterator. Instead, it's used to sort reducer input, so that the reducer knows when a new grouping starts. 

In our example, the value grouping comparator will sort by the first letter of the key. 

h5. OUTPUT KEY COMPARATOR

The OutputKeyComparatorClass JobConf setting also takes in a org.apache.hadoop.io.RawComparator. This RawComparator is used to sort the values iterator that the reducer gets, which is what we want. It should be noted, that although the RawComparator is used to sort the values iterator, the data that gets passed into the comparator is the mapper key output. This is the reason that we must put all data in the key as well as the value. 

A *very* important thing to note is that they key compartor must also enforce the value grouping comparator's rules. In our example, this means that it must first check if the first letter is equal. If it's not equal, it should return the same ruls as the value comparator. Only if the first letter of the key is equal should we apply our value-level sorting (comparing the second letter). If you do not do this, you will break your grouping. 

In our example, the key comparator will sort by the second letter of the key. 

h5. RUNNING THE JOB

Now, all we need to do is run the job.

<script src="https://gist.github.com/3775858.js"> </script>

h5. OUTPUT

As you can see, the reducer input is grouped by the first letter (our logical key), and the values are sorted ascending.

bc. AY: YWUTSSSRRQPPPPOMMKJIIIFB
BZ: ZYYXXXWVUUURRRRQPPPPPPOONMMLLKJHGEEDDBB
CZ: ZZZZZYYXXWVUUUTSSSRQQOOMKKKHHHGGFFDDCCCBB
DY: YXWWSSQQPPPONMMKIHGEDDCCBB
EW: WVUTRRRQPOOOOONMLLKKKJJHFEEDDCCBA
FY: YXXXWVVVUUTSSRPNNNLLKJHGFFECBBBBA
GZ: ZZYXVTSQQPOONLJIHHHFFCCCBBA
HZ: ZYYYYXWVUUTTTRQQPOOMKJJIIIGFEDAAAA
IY: YYYXWWVVVUTTSRRRQMKJJJIIIHGGFFEEEECBBBA
JZ: ZZYYXXWRRRQPPOOOMLJJIIHHHHCCCBBA
KZ: ZZYXWWVSSSSRQONMJIIHFEDB
LZ: ZZZYYXXWUTRQQQPLKJIIIHHGGFDDCCCBBBAA
MZ: ZZYYYWTTTSSQQQQOJIIIHGGFCCCBBAA
NZ: ZZYYXVVUTSSSSRQPNMKIHGFFFECAA
OZ: ZZZYYXWWUSRRPPOONNNMMLJIIHHHGGFEEEDDCCBA
PZ: ZXXWWTSSSSSRRRQQQMMLLLKJIIIHEEDCBA
QZ: ZZYXWWWWWWVVVUTTSSSSRRRRQQQPOOONMLKJIHHFDD
RY: YYYXXXWVUURRQQPPOOOLLLLLLKJJJJHHHHGFFEEEDDCCCBAA
SY: YXWWWVVVUUUTTSRRRQQQNNNMLJHHHGGGGFEDDCCCBB
TZ: ZZYYYYXXWVTTTTSRRQPPONNNNMMLLJIIIICBB
UZ: ZZZYXWWVVVSRRRQPPONMHHGEDCBBA
VZ: ZYWVVUTTTQPPPOOMKIIGFEEDDCCCBB
WX: XWWWVUTTSSSRRPNNNMMLLKKKKKJJIGEDAAAA
XZ: ZZYXXXXSSRRQQOOMLLKKJIIIIHGFFEDDBA
YZ: ZZZYXWWVUUUTTTSSRQPPPOONNNMLJIIFFFFEDCCCAA
ZZ: ZYYWVVUUTSSSSRRQQQPOONMMLLLJJIIGFDBBBA

h5. LINKS

"Owen O'Malley's Value Sorting Email":http://markmail.org/message/7gonm3kiasyh2xnf#query:setOutputKeyComparatorClass+page:3+mid:esn3lgzyx3ag26cy+state:results
"Hadoop Value Grouping Example Patch":http://issues.apache.org/jira/secure/attachment/12356648/485.patch
"Secondary Sort Hadoop Example":https://issues.apache.org/jira/browse/HADOOP-4545
