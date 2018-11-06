---
layout: post
title:  "Sorting Reducer Input Values in Hadoop"
author: chris
categories: [ distributed-systems, hadoop ]
image: assets/images/2009-11-13-sort-reducer-input-value-hadoop/hadoop-logo-png-transparent.png
redirect_from:
  - /posts/hadoop/2009-11-13-sort-reducer-input-value-hadoop/
---

I HIGHLY recommend that you read the email thread by [Owen O'Malley](http://markmail.org/message/7gonm3kiasyh2xnf#query:setOutputKeyComparatorClass+page:3+mid:esn3lgzyx3ag26cy+state:results) that describes this technique in brief. I should also note that this example is using the 0.18 Hadoop API. 

## Problem statement

Suppose we have a file with a bunch of comma/line separated letters:

```
l,f,a,e,a,a,l
f,g,b,c,b,d,f
x,i,t,u,f,e,h
...etc
```

We want our reducer to receive bigrams (lf, fa, ae, ea, aa, al, etc), but partitioned by the first letter, and sorted (ascending) by the second. For example, for the letter a, the reducer should receive:

```
<a, [l,e,a]>
```

This is actually somewhat difficult to do, since we want to partition by key, but sort the reducer's values iterator. The trick is to have the mapper output the bigram in the key, and only the second letter in the value. For the example above, the mapper would emit:

```
<ae, e>
<aa, a>
<al, l>
...
```

We can then use a custom partitioner/sorter to partition and sort according to our needs. 

{% include newsletter.html %}

## Sorting by value

To sort Hadoop's mapper output by value, you need to set three settings in your JobConf:

* setPartitionerClass
* setOutputValueGroupingComparator
* setOutputKeyComparatorClass

There are many threads that say that you can't sort by value in Hadoop. This is true. What you can do, instead, is have your mapper output all data in the key, rather than the value. Then you can use a specialized Partitioner classes and two RawComparator classes to sort and partition your map output properly. 

## Partitioner

The first class that you need to set is a class that extends org.apache.hadoop.mapred.Partitioner. This class has a single function that determines which partition your map output should go to. This means that you can't go below 0, or above numPartitions - 1. Mostly, you'll want to hashCode() some portion of your key and mod it by numPartitions. 

In our example, the partitioner will partition by the first letter of the key. 

## Output value grouping comparator

The OutputValueGroupingComparator JobConf setting takes in a org.apache.hadoop.io.RawComparator. This RawComparator is used to determine which reducer the mapper output row should go to. This RawComparator does not sort a reducer's value iterator. Instead, it's used to sort reducer input, so that the reducer knows when a new grouping starts. 

In our example, the value grouping comparator will sort by the first letter of the key. 

## Output key comparator

The OutputKeyComparatorClass JobConf setting also takes in a org.apache.hadoop.io.RawComparator. This RawComparator is used to sort the values iterator that the reducer gets, which is what we want. It should be noted, that although the RawComparator is used to sort the values iterator, the data that gets passed into the comparator is the mapper key output. This is the reason that we must put all data in the key as well as the value. 

A *very* important thing to note is that they key compartor must also enforce the value grouping comparator's rules. In our example, this means that it must first check if the first letter is equal. If it's not equal, it should return the same ruls as the value comparator. Only if the first letter of the key is equal should we apply our value-level sorting (comparing the second letter). If you do not do this, you will break your grouping. 

In our example, the key comparator will sort by the second letter of the key. 

## Running the job

Now, all we need to do is run the job.

```java
public class SortReducerByValues {
	public static final String INPUT = "/tmp/data_in";
	public static final String OUTPUT = "/tmp/data_out";
	
	public static void main(String[] args) throws IOException {
		new SortReducerByValues().run();
	}
	
	public void run() throws IOException {
		JobConf conf = new JobConf();
		
		conf.setInputFormat(SequenceFileInputFormat.class);
		conf.setOutputFormat(SequenceFileOutputFormat.class);
		
		conf.setMapOutputKeyClass(Text.class);
		conf.setMapOutputValueClass(Text.class);

		conf.setOutputKeyClass(Text.class);
		conf.setOutputValueClass(Text.class);

		conf.setMapperClass(SortReducerByValuesMapper.class);
		conf.setReducerClass(SortReducerByValuesReducer.class);

		conf.setOutputKeyComparatorClass(SortReducerByValuesKeyComparator.class);
		conf.setOutputValueGroupingComparator(SortReducerByValuesValueGroupingComparator.class);
		conf.setPartitionerClass(SortReducerByValuesPartitioner.class);

		FileInputFormat.addInputPath(conf, new Path(INPUT));
		FileOutputFormat.setOutputPath(conf, new Path(OUTPUT));
		
		conf.getWorkingDirectory().getFileSystem(conf).delete(new Path(INPUT), true);
		conf.getWorkingDirectory().getFileSystem(conf).delete(new Path(OUTPUT), true);
		
		loadFakeData(INPUT);
		
		JobClient.runJob(conf).waitForCompletion();
	}
	
	public static final class SortReducerByValuesKeyComparator implements RawComparator {
		public int compare(byte[] text1, int start1, int length1, byte[] text2, int start2, int length2) {
			// hadoop gives you an extra byte before text data. get rid of it.
			byte[] trimmed1 = new byte[2];
			byte[] trimmed2 = new byte[2];
			System.arraycopy(text1, start1+1, trimmed1, 0, 2);
			System.arraycopy(text2, start2+1, trimmed2, 0, 2);
			
			char char10 = (char)trimmed1[0];
			char char20 = (char)trimmed2[0];
			char char11 = (char)trimmed1[1];
			char char21 = (char)trimmed2[1];
			
			// first enforce the same rules as the value grouping comparator
			// (first letter of key)
			int compare = new Character(char10).compareTo(char20);
			
			if(compare == 0) {
				// ONLY if we're in the same reduce aggregate should we try and
				// sort by value (second letter of key)
				return -1 * new Character(char11).compareTo(char21);
			}
			
			return compare;
		}

		public int compare(Text o1, Text o2) {
			// reverse the +1 since the extra text byte is not passed into
			// compare() from this function
			return compare(o1.getBytes(), 0, o1.getLength() - 1, o2.getBytes(), 0, o2.getLength() - 1);
		}
	}
	
	public static final class SortReducerByValuesPartitioner implements Partitioner {
		public int getPartition(Text key, Text value, int numPartitions) {
			// just partition by the first character of each key since that's
			// how we are grouping for the reducer
			return key.toString().charAt(0) % numPartitions;
		}

		public void configure(JobConf conf) { }
	}
	
	public static final class SortReducerByValuesValueGroupingComparator implements RawComparator {
		public int compare(byte[] text1, int start1, int length1, byte[] text2, int start2, int length2) {
			// look at first character of each text byte array
			return new Character((char)text1[0]).compareTo((char)text2[0]);
		}

		public int compare(Text o1, Text o2) {
			return compare(o1.getBytes(), 0, o1.getLength(), o2.getBytes(), 0, o2.getLength());
		}
	}
	
	protected void loadFakeData(String path) throws IOException {
		JobConf conf = new JobConf();
		Writer writer = SequenceFile.createWriter(FileSystem.get(conf), conf, new Path(path), Text.class, Text.class);
		
		for(int i = 0; i < 100; ++i) {
			String letterCSV = "";
			
			for(int j = 0; j < 10; ++j) {
				letterCSV += (char)(65 + (int)(Math.random() * 26)) + ",";
			}

			writer.append(new Text(), new Text(letterCSV.substring(0, letterCSV.length() - 1)));
		}
		
		writer.close();
	}
	
	public static final class SortReducerByValuesMapper implements Mapper {
		public void map(Text key, Text val,
				OutputCollector collector, Reporter reporter)
				throws IOException {
			String[] chars = val.toString().split(",");
			
			for(int i = 0; i < chars.length - 1; ++i) {
				collector.collect(new Text(chars[i] + chars[i+1]), new Text(chars[i+1]));
			}
		}
		
		public void configure(JobConf conf) { }
		public void close() throws IOException { }
	}
	
	public static final class SortReducerByValuesReducer implements Reducer {

		@Override
		public void reduce(Text key, Iterator values,
				OutputCollector collector, Reporter reporter)
				throws IOException {
			// values should now be in order
			String check = key + ": ";
			
			while(values.hasNext()) {
				check += values.next();
			}
			
			System.err.println(check);
		}

		public void configure(JobConf conf) { }
		public void close() throws IOException { }
	}
}
```

## Output

As you can see, the reducer input is grouped by the first letter (our logical key), and the values are sorted ascending.

```
AY: YWUTSSSRRQPPPPOMMKJIIIFB
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
```

## Links

* [Owen O'Malley's Value Sorting Email](http://markmail.org/message/7gonm3kiasyh2xnf#query:setOutputKeyComparatorClass+page:3+mid:esn3lgzyx3ag26cy+state:results)
* [Hadoop Value Grouping Example Patch](http://issues.apache.org/jira/secure/attachment/12356648/485.patch)
* [Secondary Sort Hadoop Example](https://issues.apache.org/jira/browse/HADOOP-4545)
