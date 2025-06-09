# ResearchRouter: routing research questions to the right people

<p align="center">
  <img src="https://sdmntprwestus2.oaiusercontent.com/files/00000000-4428-61f8-9eae-592cf6d09851/raw?se=2025-06-09T01%3A01%3A18Z&sp=r&sv=2024-08-04&sr=b&scid=48273da1-5a32-5405-a804-3982b0f26777&skoid=61180a4f-34a9-42b7-b76d-9ca47d89946d&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-06-08T23%3A13%3A38Z&ske=2025-06-09T23%3A13%3A38Z&sks=b&skv=2024-08-04&sig=bXBM1CNdFW5whYKq64wX6adaFnjJtcQyvYP6BN9fWeo%3D" alt="ResearchRouter Logo" width="400"/>
</p>


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