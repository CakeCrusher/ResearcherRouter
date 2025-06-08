# ResearchRouter: routing research questions to the right people

The community at SPS is generally composed of members actively engaged in several areas of research but knowing who is the right person to talk to for knowledge transfer is neither accurate nor efficient.

## Solution

We will use the `cool-papers` channel as an index for our collective knowledge of research. We will use this collective knowledge and map the experts to the corresponding subjects such that whenever somebody has a question on a subject they can easily find a member that they can reach out to for answers.

## Technical Implementation

- Vector store
  - stores vectors of research material with relevant members in metadata
  - search vector store against prompt to surface relevant research and consequently relevant members
- Interface to Discord
  - Forum migration on `cool-papers` channel for ingesting data, uses the discord `guild` as database through forum properties  
  - @bot interface to ping (potentially) knowledgeable researchers to a query
- Deploy discord bot (forum migration)

## Resources

- [Figma](https://www.figma.com/board/ejeHzoSBKpxafkRqzt0rk8/ResearcherRouter?node-id=1-28&t=VVCTcXmk0rwvn9Zd-1)