# Debug database

The purpose of the debug database is to track operator transformations during
the optimisation process of Vela. This is later correlated with the trace
output of the model, externally, to determine the runtime of the original layer
operators. Standalone, the debug database can be used in order to give a brief
overview of how the operators in the network change throughout the optimisation
process. This document gives an overview of the structure of the database and
its outputs, to help parsing of the generated data in a debug procedure.

# Contents

While processing, Vela maintains information about operator substitutions and
command generation in its internal Debug Database. The database tracks the data
transformations through the following states:

- Creation of Source operators - these operators are created from the source
representation,  in this case the original TFLite file.
- Creation of Optimised operators - these are the operators that result from
 optimising the source operators. They may be the source operators repeated,
or substitute operators inserted by the optimiser.
- Creation of Queue commands - these are the register command sequences
generated by the code generator from the optimised operators.

Vela's processing steps add data to internal debug tables; one table for each
of the above states. When vela has completed processing, it can write out the
internal debug tables through the command line option "++enable-debug-db".

# File Format

The internal debug tables are formatted as columnar CSV. Each row represents an
operator or stream command; keyed on a numeric value that uniquely identifies
that operator or command. These tables are further packaged into an XML
container file, along with metadata, for easier transport and handling.

**Debug node**

The top-level debug node wraps the entire file and contains information about
the source and optimised file paths.

<debug optimised="output_from_vela.tflite" source="input.tflite">

**Table nodes**

The top-level debug node contains one or more table nodes. Each table node is
named, and the table data is represented as CSV formatted text stored in a
CDATA payload tag. The first row of the table contains column headers.

<table name="source"><![CDATA[ "column0", "column1", "column2", ...

There currently are 4 named tables.

- "source" - Table of TFLite operators from the source file.
- "optimised" - Table of optimised operators generated by vela
- "queue" - Table of command queue offsets
- "cmdstream" - Table describing properties of one or more command streams


The tables reference each other through the following connections: the Queue
table is linked to the Optimised table through the *optimised_id* and the
command stream table through the *cmdstream_id*. The Optimised table is in turn
linked to the Source table through the *source_id*.

# Ordering

Note that the source, cmdstream and optimised tables are not ordered in a
meaningful way. The insertion order of entries in the source and optimised
tables is arbitrarty - a side effect of traversal and optimisation. No attempt
should be made to interpret the entries as a graph. The only ordered table is
the queue table; which is ordered by its queue offset. This table describes the
execution order of the hardware commands, and they can be mapped back to the
optimised and source operators in order to determine their execution order.