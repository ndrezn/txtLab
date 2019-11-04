## 5-9-19
* collect the total edits for each set 
* collect the total large vandalism for each set
* optimize word counter using multiprocessing
* for later: 
	* retrieve the average length of each edit for each set
	* calculate the number of unique users vandalizing

## 5-10-19
* collect average length of each edit for each set
	* found a high average length for each edit. So... am I wrong, or is something interesting happening? To check: Identify long edits and scan for patterns.
	* Is more text indicative of more happening?
* isolate large sized edits to see if they are interesting (they are not super interesting)
* for later:
	* confirm math for the length of each edit (test the same thing in other places)

## 5-13-19
* Count/visualize the number of edits of certain sizes (1-25 words, 24-50 words, 50-75 words, 75+ words)
* for tomorrow: isolate edits made by bots

## 5-14-19
* Identify reversions by finding the word "revert" / "undid" in comments.
	* Separate reversions made by bots from reversions made by users.
* generate lists of most prominent users in each space

#### Meeting with Andrew
* time frequency between edits. For a given field, average time between every edit?
	* how hotly debated things are.
	* Overall number of edits, time between edits, average number of words edited.
	* Experiment with box plots to plot each of these out. Anova test. Given the medians of these three worlds & variance between them, would we make a judgement that one or more is behaving differently? 
	* Treat those three culture things as one group: Look at three lists from each domain. (Intercultural assessment vs. domain assessment). We assume that political discourse is more hotly edited than cultural. 
		* People who talk about novels are more isolated than film and television. Two people get an edge when they both edit the same page, label edges by medium. Every time you edit a novel together, etc. Check to see if world is well connected to itself. 
		* Each node represents a work. Weight increases when an editor edits two pages. 
			* If people who edit novels only edit novels and not film/tv, then there should be clusters: Those works won't be connected to other works. Communities that are predicted could have low accuracy. Say something about homogeneity of two sets. Associativity (extent to which two nodes belong to the same class are connected). Homophaly. Are we omnivorous culturally?
* Use 2-gram/3-gram analysis. Measure distinctiveness.
* Next step: What is the time/infrastructure required? Leg work of finding parallel lists for other domains. For Thursday, collect the other domains. 4-5 other social domains. What are the 3-4 lists of pages that can be used for this? Sports, politics, science, culture, etc. Intuitive/common nonsensical domains.

## 5-15-19
* Generate sets of pages for other social domains. 
* 2-gram/3-gram analysis on changes/constant.
* Social networks of editors, where pages are nodes, edges are number of editors who edited both pages, and nodes are colored by cultural domain.

## 5-16-19
* Finish generating visual social networks based on users
* Scrape urls of other social domains.

#### Group meeting
* Assortitivity/modularity tests on graphs. How well do inferred communities align with genres.
* x-axis is person, y-axis is number of edits. Quantify where to cut it off and get rid of the most active editors. Elbow test. Finds the natural breaks. Louvain community detection. Export model files. Read into Gephi.
* Cultural omnivore. Higher level concepts: Understand how a community behaves based on their editorial habits, which include discursive habits. Find relationships between word usage and community structure. 
* Classifiers! Words people use for books and predict on movies/tv. When testing discursive continuity... Classifier learns the difference between book edits and non book edits. Then test on film. Given a discursive domain of editing on books, how well can that map onto editing in film? We can show structural overlap but different language domains. We aren't just consumers, but have a lexical range with a different set of fluent lexical registers.
* MDW vs. logistical regression!
* Language of cultural discourse vs. behavior.
* Things discussed in a prominent way favor WHAT kind of language? e.g. academics talking about Morrison start using her words.
* Next week: Graph work. Scrape from other domains. Send domain list to Andrew & Richard.
	* Lesson from Richard next Friday. 

## 5-17-19
* Collect edit counts for all users
* Work with graphs in Gephi

## 5-21-19
* Elbow test on user counts
* Modularity test with raw graph. Find three sets that align almost perfectly with the three genres.

## 5-22-19
* Visualize editor counts
* Work through list of users

## 5-23-19
* Switch to Jenks natural breaks optimization instead of k-means to define data clusters & user groups; 528445 total users 
	* Using edges, 10 breaks: [1.0, 1.0, 4.0, 10.0, 20.0, 35.0, 58.0, 90.0 (159 users), 140.0 (67 users), 207.0 (14 users), 276.0]
	* Using edits, 10 breaks: [1.0 (189731), 28.0 (5308), 138.0 (994), 385.0 (316), 858.0 (96), 1840.0 (32), 3537.0 (9), 5958.0 (3), 8692.0 (2), 15514.0 (1), 19005.0 (0)]

## 5-27-19
* Generate new graphs with upper cutoff users removed.

### Call Andrew
* Put numbers to each steps. Made a cut at 28 edits, this accounts for what percentage of all edits. Working through the data, keep a facts sheet. Record the consequences of each step. 
* Purity and entropy measure how coherent a class is. Assume it has one identity, how much of a class has that identity? Assume everyone is talking 
* Identity of every node is a page that belongs to a medium. For each community, what percentage of each node is in each medium. Assumption is each community should allign to a single medium. How imperfect is this? Given the dominant class for a community, what percentage of all pages in the community are books? Entropy measures how mixed that class is. Maximum entropy is when each group is equally balanced. 
	* How well set are each set?
* Social spheres
	* From a social network perspective: How much do people from one domain edit pages from another domain? Apples-oranges doesn't matter for this question.
	* Intensity. Does not necessarily depend on a genre.Trying to avoid confounders. Is there something about a genre that elicits fewer responses?
	* When people argue about science, what language do they condition on as opposed to when they argue about culture? Or, in biography, studying traction on debates in LIVES.
	* What are the aspects of lives conditioned on that don't have to do with the domains themselves? There are ways to filter vocabulary: Find words unique to an author, and lower the feature weights of those items. Do something similar: In biography pages, lower the features from the domain, establish a vocabulary model of science/art pages. Adjust the features in the model down from those things. 
		* i.e. Take the science words out of science biographies. What's left?
	* "great": how does the word appear?
	* Control for more specific domains. Pick a branch of science, not science in general. Physicists/chemists, etc. 
	* "Cultures of debate." Frequency + volume = intensity.
* Generate a road map: Solve problems instead of generating more.
	* Two measurements of intensity: More edits/more frequent edits means people are more hot + bothered. 
	* Community coherence. How much cross-domain behavior is there? Either within the arts or from arts to other fields. (Social network & semantic question) We found that behaviorally these are very strong communities. Given behavior, can I predict communities? Yes! Given communities, can I predict them based on semantic behavior? 3-way classifier. Given training data, machine learns what an edit looks like for a film, novel, etc. How easy is it to predict the proper class based on the words? Compare the purity of the communities to the accuracy of the classifier. If they aren't equivalent, people's choices are more legible. Interaction overlaps more than editorial behavior. Both cases ask about community coherence from different points of view.
	* What is the language lay-users care about when compared to popular domains and academic domains? Compare Wikipedia writing to non-Wikipedia domains (JSTOR). 
		* Take three biggest science sets. Use Wikiprojects. 
		* Sports, culture, politics, science.
	* In-domain analysis. What's the likelihood that someone who edited something from the 19th century edited something from the 20th century. Do people cluster around certain genres or periods when they edit things? 
	* Do people debate Victorian fiction more than modern novels? What TV shows inspire the most debate?
	Inside each unit, there are more questions to be asked. What would people like to know about this data?
* Riddles project: Poem similarity
	* Jury is out on the best way to do this. Hard to asses whether extra steps for poem similarity is necessary. Simplest thing to do is a windowed approach for text similarity. Kulback Libler divergence. (KLB divergence). Measures how much information is lost when you approximate one probability distribution by another. Divergence score. Probability distributions are observed word frequencies in a corpus. Set A is all documents from a 10 year period, represented as a list of words & their frequencies. Normalize by the length of the documents. Do that for the next 10 year window. Two distributions that can be compared. From 1900 to 1905, how much information is lost when I approximate that to 1905 to 1910. Slide forward taking 5 year windows, which can show that things are the same or changing. Question of the significance of change is a new problem. 1901 to 1906 compared to 1907 to 1911. Gives an estimate of when the period of change occurred. Once you find that peak point of change, use the vocabulary test to find what is distinctive of that set. 
	* Simplest measure of complexity: Vocabulary richness. Word length. Sentence length. Use a package in r called "koRpus:" suite of reading difficulty measures. Plenty of  formulas that condition on word length, syllable length/count, sentence length. Flesh reading ease. Used to study the difficulty. Small data problem, should wash out. If you have more things, the differences could be more or less. Language will pile in and get less disjointed. Differences between any two texts is large, but between all texts is small.

## 5-28-19
* Work with other clustering algorithms. Learn about dendrogram structures.

## 5-29-19
* Run with all clustering algorithms.
	* Distributions:
	* spinglass
		{'films': 1, 'tv': 1, 'novels': 96}
		{'films': 2, 'tv': 95, 'novels': 0}
		{'films': 90, 'tv': 0, 'novels': 0}
		{'films': 0, 'tv': 0, 'novels': 1}
		{'films': 0, 'tv': 1, 'novels': 0}
	* multilevel
		{'films': 0, 'tv': 4, 'novels': 96}
		{'films': 92, 'tv': 0, 'novels': 0}
		{'films': 1, 'tv': 93, 'novels': 1}
	* infomap
		{'films': 93, 'tv': 97, 'novels': 97}
	* fastgreedy
		{'films': 1, 'tv': 0, 'novels': 96}
		{'films': 2, 'tv': 97, 'novels': 1}
		{'films': 90, 'tv': 0, 'novels': 0}
	* walktrap
		{'films': 0, 'tv': 13, 'novels': 67}
		{'films': 12, 'tv': 82, 'novels': 29}
		{'films': 81, 'tv': 2, 'novels': 1}
* Start scrape for all novels from the list, sorted by year

## 5-31-19
* Run full scraper for films
* Create social network for novels
* Group meeting

## 6-3-19
* Start messing with full novel data set

## 6-4-19
* Likelihood two people edited two pages links--the more coherent, the more likely people are editing within a genre. What's the coherence around time or genre?
* Use Louvain model for communities. We did medium. 
* Assortitivitiy: likelihood that if node a is connected to node b that they are in the same class.
* Test assortivity on a random set using genre or time and a subset of novels, tv, or films.
* Take the same number of edits from each document. 
	* Question about how do document behave vs. how do people behave? Take samples that control for the unfair distribution. If I take an even sample out of documents, will I find the same patterns?

## 6-6-19
* Plan: Test assortitivity for random set of novels, tv, films. Test purity of medium.
	* Separately: Test assortivity for random set of novels or tv or films. Test purity of genre & time.
* To-do: Connect metadata sheet to files. Build assortivity test for graphs.
* Concerns with number of classes in modularity. Medium has 3, genre has more than 3, etc. Assortativity is more stable. Gives correlation coefficient. Run that for each test, giving some estimation of which is the strongest driver of assortivitiy.
* What is the strength & coherence of these categories based on these. Next: how coherent are these communities from a linguistic perspective? Classification will be useful here. Train on a category, predict on the others. Train on all three, see how predictable they are. Get the predictive power of each category given the language?
* Gotta learn logistic regression. 
* Run classification on the language of the edits. 
	* Treat all the edits of a page as a bag of words. Belongs to either medium, genre, or time period. Classify & predict based on those bags of words!

## 6-10-19
* Finish scrape of novels, tv. Compile tv, films added words into txt files.

## 6-11-19
* Working on classifier. Use [this](https://www.analyticsvidhya.com/blog/2018/04/a-comprehensive-guide-to-understand-and-implement-text-classification-in-python/) tutorial.
* __NB, Count Vectors:  0.9381147088076031__
	* Count Vector is a matrix notation of the dataset in which every row represents a document from the corpus, every column represents a term from the corpus, and every cell represents the frequency count of a particular term in a particular document.
* __NB, WordLevel TF-IDF:  0.9313736324455741__
	* Matrix representing tf-idf scores of every term in different documents
	* TF-IDF score represents the relative importance of a term in the document and the entire corpus. TF-IDF score is composed by two terms: the first computes the normalized Term Frequency (TF), the second term is the Inverse Document Frequency (IDF), computed as the logarithm of the number of the documents in the corpus divided by the number of documents where the specific term appears.
* __NB, N-Gram Vectors:  0.9088297049397723__
	* tf-idf of N-grams. Not really applicable to this situation, since it's just a bag of words model. N-grams don't matter.
* __NB, CharLevel Vectors:  0.849486131064206__
	* Character-level n-grams. Again not really applicable.

## 6-12-19
* Work on getting the classifier to work with genre, year. Having issues with this. Dataframes suck!
* Classifying based on year (using 25-year increments). Run accuracy test 5 times, take average:
	* I had results here but they were incorrect so they're now deleted
* Work on Amazon scraper

## 6-13-19
* Find captcha bug in Amazon scraper
* Create proper metadata sheet for TV
* Run classifier using TV
	* Had results here but they were incorrect so they're now deleted.

## 6-14-19
* Classification results using a sample of 200 texts from each:
* medium
	* NB, Count Vectors:  0.8238993710691824
	* NB, WordLevel TF-IDF:  0.8553459119496856
	* LR, Count Vectors:  0.9308176100628931
	* LR, WordLevel TF-IDF:  0.9308176100628931
* genre (films & tv)
	* NB, Count Vectors:  0.5753424657534245
	* NB, WordLevel TF-IDF:  0.45205479452054786
	* LR, Count Vectors:  0.4794520547945205
	* LR, WordLevel TF-IDF:  0.4794520547945205
* genre (tv)
	* NB, Count Vectors:  0.6341463414634145
	* NB, WordLevel TF-IDF:  0.41463414634146345
	* LR, Count Vectors:  0.5121951219512194
	* LR, WordLevel TF-IDF:  0.41463414634146345
* genre (films)
	* NB, Count Vectors:  0.4242424242424242
	* NB, WordLevel TF-IDF:  0.3636363636363637
	* LR, Count Vectors:  0.393939393939394
	* LR, WordLevel TF-IDF:  0.3636363636363637
* year
	* base of 50
	* NB, Count Vectors:  0.5869565217391306
	* NB, WordLevel TF-IDF:  0.48550724637681164
	* LR, Count Vectors:  0.6666666666666667
	* LR, WordLevel TF-IDF:  0.6449275362318839
* year
	* base of 25
	* NB, Count Vectors:  0.2391304347826087
	* NB, WordLevel TF-IDF:  0.10869565217391305
	* LR, Count Vectors:  0.18115942028985504
	* LR, WordLevel TF-IDF:  0.10144927536231885

### Meeting with Richard & Andrew
* What is the strength & coherence of these categories based on these.
* Statistical Consulting McGill for stats help!
* For next week: Test purity using year & genre metrics in addition to medium. Test using the larger dataset (of all the nodes?)
* Collect the most distinctive features. 
* Get the significance / p value for class identification.
	* Look at the existing number of genres, merge them if they're similar.
* Looking at most significant features: Look for signs & signals that won't convince people. Try classifying only with stop words. Try part of speech tags using spacey. Try bi-grams instead of unigrams.
* When making comparitive statemts (is medium more distriminant than period?), make them comporable--make them the same number of classes. 
* Big cultural hypothesis: Lionel Trilling (*The Liberal Imagination*). Hypothesis: Politics is a degraded way to talk about stuff. It's politics without political thought. It's only in culture & literature where thinking about form allows political thinking. There might be complex thought happening in people talking about TV shows vs. in politics. e.g. when we talk about sexuality in *Game of Thrones* it's more sophisticated than when we talk about sexuality in politics.
	* Politics, science, culture, and sports. Looking for general contentiousness levels, then embattle topics.
	* Topic model the edits in each domain. This should surface the larger-scale fields of debate. 
* Use cross-validation, not one-against-all.
* Make a CSV with the starting url and the name of the genre for all the genres.

## 6-27-19
* Restructure github repository
* Re-collect all added words for films
* Build functionality for So's classifier in order to capture most distinctive traits of each set.

### Meeting w/ R&A
* Counterfactuals. Use excercises where you take out strong classifying language and see if the classifier still works well.
* For part of speech tagging: Spacey. Stanford Core NLP works better for long texts. Parts of speech: think of bi- and tri- grams. 
* Zoom out!
	* Biggest question on Wiki: What are people arguing about?
	* Intensity. What is the relative intensity surrounding a document or field? 
	* Intensity, community coherence, and Wikipedia culture.
* Long term: Poster is a first-draft for the white paper. Bare rudiments of four to five quadrands. Use that in a discursive way--practice public writing. 
* In two weeks: Put together a mini-powerpoint. Findings, questions, brief statements/graphs/charts. 

## 7-2-19
* Continue working with classifier

## 7-3-19
* Continue working with classifier

## 7-4-2019
* Get multiclass feature idenfitication working

### Meeting with Richard
* figure out if multiclass feature idenfitication is possible
	* Report features for pairwise comparisons. 
		* Compare novels-films, films-tv, novels-tv and report the distinctive features for each set.
	* Underlying is that it's a binary case so you have to futz it.
	* Document sampling techinque, document sampled values. 
		* To deal with large sets: Set CB as 5-10.

## 7-8-19
* Collect features for pairwise comparisons.
* Prep thoughts on using word2vec
* Go back to working with graphs -- generate purity ratings
	* Testing genre: 
* ideas for visuals
	* Classification:
		* Plot binary comparisons by year of publications. One-versus-all model. 

## 7-9-19
* Distinguishing features of novels vs. films: (Mean: 0.9550334801725804, Stdev: 0.008570440967511445)
	* Novels: grossi (1.940), finalists (1.663), illustrates (1.584), republishing (1.528), publishersweekly (1.502), sfa (1.456), kirkusreviews (1.455), tora (1.432), isbndb (1.431), goodrich (1.425), novelistic (1.424), reprinting (1.423), serially (1.422), locusmag (1.403), publisher (1.371), gutenburg (1.370), bookloons (1.354), spent (1.326), authorative (1.304), bestsellers (1.299)
	* Films: silentbobspeaks (0.569), starrring (0.596), imdbpro (0.618), goldy (0.634), technicolored (0.641), distributer (0.694), redirected (0.699), dramaadventure (0.702), croy (0.706), directedby (0.717), westerner (0.767), archived (0.768), monogrammed (0.777), zumbrunnen (0.809), mgr (0.813), taglines (0.814), filmonic (0.817), rkos (0.825), dwane (0.831), comedyfilm (0.837)
* Distinguishing features of novels vs. tv (Mean: 0.9642286308900091, Stdev: 0.00957714073386161)
	* TV: redirected (3.281), wih (3.166), laster (1.817), rana (1.484), nbcuniversal (1.476), cbsnews (1.476), canceling (1.472), liveing (1.406), starrett (1.382), cancelling (1.352), starrs (1.260), lifetimes (1.193), filmer (1.192), piloted (1.190), premieredate (1.168), westerosi (1.166), lineups (1.156), wbbm (1.155), aires (1.133), mosaics (1.130)
	* Novels: authorative (0.712), novela (0.799), stocked (0.818), adapter (0.826), publisher (0.865), spoilerabout (0.874), trim (0.883), bookscan (0.895), editable (0.896), novelswikiproject (0.902), fictionabsurdist (0.902), deletions (0.921), shipboard (0.922), sciencefiction (0.927), articleexpired (0.930), meekly (0.930), planeta (0.935), booka (0.937), writtenby (0.938), hardys (0.942)
* Distinguishing features of TV vs. film (Mean: 0.9709028114886498, Stdev: 0.008273662438197354)
	* TV: foxnews (2.083), sitcomabout (1.684), unalienable (1.676), cancelling (1.672), redirected (1.668), canceling (1.611), cancellations (1.602), laster (1.543), directs (1.518), cbsnews (1.431), filmbased (1.363), rana (1.315), lineups (1.306), liveing (1.299), nbcuniversal (1.299), starrer (1.271), developers (1.252), res (1.191), lifetimes (1.176), ufos (1.161)
	* Film: silentbobspeaks (0.540), directedby (0.741), starrng (0.852), tobacconist (0.915), technicolored (0.920), mgmt (0.926), performed (0.930), picturesamblin (0.932), wealty (0.933), charleses (0.936), uncreditted (0.941), rkos (0.945), broadwayworld (0.950), foreignally (0.950), olsens (0.953), screenplays (0.955), westerner (0.956), jeana (0.956), artless (0.957), romantically (0.957)

* Film genres: 
	* Drama: 6392
	* Comedy: 5057
	* Western: 2938
	* Horror: 854
	* Adventure: 754
	* Action: 689
	* Crime: 661
	* Musical: 647
	* nan: 566
	* Thriller: 533
	* Mystery: 496
	* Crime drama: 461
	* Documentary: 459
	* Romance: 413
	* Romantic comedy: 389
	* Film noir: 371
	* Science fiction: 367
	* War: 300
	* Animation: 260
	* Animated: 212
	* Family: 188
	* Musical comedy: 188
	* Sci-fi: 186
	* Comedy, Drama: 179
	* Biography: 169
	* Fantasy: 144
	* Melodrama: 115
	* Comedy-drama: 111
	* Drama, Crime: 109
	* Suspense: 104
* TV genres:
	* comedy: 522
	* drama: 153
	* crime drama: 121
	* reality: 100
	* animation: 93
	* science fiction: 53
	* action: 48
	* competition: 44
	* western: 42
	* Comedy: 41
	* talk show: 38
	* situation comedy: 31
	* animation comedy: 31
	* medical drama: 30
	* comedy/drama: 25
	* Animation: 24
	* legal drama: 23
	* variety: 20
	* teen drama: 20
	* teen comedy: 19
	* soap opera: 19
	* Drama: 19
	* science-fiction: 18
	* police procedural: 18
	* sketch comedy: 17
	* nan: 16
	* Competition: 16
	* Reality: 14
	* police drama: 13
	* supernatural: 11
	* mystery: 11
	* Action: 11
	* comedy-drama: 10

* Classification by period
	* Television (Split point: 1999)
		* Mean: 0.8439030763686737, Stdev: 0.04119794239219875
		* Features of second class (late period?)
			* premieredate (1.335), criticise (1.150), swore (1.132), aaa (1.119), templatequotecite (1.104), wbshop (1.102), hasbro (1.096), willam (1.094), viewes (1.088), isaac (1.086), channeling (1.083), samer (1.076), styles (1.074), onassis (1.062), toadies (1.060), muppetelevision (1.055), gaye (1.054), millionare (1.054), announcements (1.052), seasoncite (1.051)
		* Features of the first class (early period?)
			* runaways (0.699), starrs (0.774), releasing (0.793), tvb (0.863), aa (0.894), whick (0.897), cc (0.907), whenever (0.916), juliet (0.919), yank (0.930), thn (0.934), abcdefghijklmnopqrstuvwxyz (0.935), sitcomcomedy (0.943), nbn (0.944), spaced (0.944), themes (0.944), warnermedia (0.945), dvdtalk (0.946), kingdoms (0.948), bobeck (0.951)
	* Films (Split point: 1950)
		* Mean: 0.8935844877408059, Stdev: 0.011494541148565303
		* Features associated with second class (late period)
			* cinemassacre (5.244), redirecting (3.075), festive (1.854), cancelation (1.747), spoilerend (1.652), globo (1.636), rottentomatoes (1.557), internationally (1.531), externals (1.507), thrillers (1.481), composers (1.458), koreatown (1.444), tagling (1.432), shepherd (1.405), cormorant (1.404), tomatoescite (1.398), funneled (1.383), shellfish (1.381), tvb (1.375), eberts (1.373), 
		* Features associated with first class (early period)
			* preached (0.439), silentenglish (0.449), preserves (0.567), codebooks (0.597), profitable (0.657), filmore (0.659), corporatism (0.675), beesley (0.683), surviviors (0.684), region (0.694), rl (0.698), remainder (0.699), archivedate (0.702), brentford (0.708), nuggets (0.714), feautres (0.722), librettist (0.728), melodramatic (0.743), montford (0.749), virginie (0.763)
	* Novels (Split point: 1989)
		* Mean: 0.786094744627164, Stdev: 0.02988516610767814
		* Features associated with second class (early period)
			* weeks (2.630), positives (1.598), scheduling (1.594), torah (1.540), aiello (1.511), harden (1.405), onlookers (1.372), debutante (1.351), webster (1.340), turturro (1.334), allie (1.321), bookmaking (1.268), releasing (1.243), meara (1.238), announcements (1.235), graendal (1.226), paulus (1.223), cabana (1.214), crimean (1.213), killmaster (1.205), 
		* Features associated with first class (late period)
			* illustrating (0.533), serials (0.577), grossly (0.688), macdougall (0.688), coping (0.735), willed (0.743), adapting (0.745), drugstores (0.760), originaly (0.772), mcgillis (0.773), originally (0.785), hamish (0.786), publishers (0.808), repudiate (0.808), editon (0.810), peril (0.816), dunce (0.821), verso (0.828), baskervilles (0.831), westerners (0.836)

## 7-10-19
* Build new metadata frame with lots of information
	* Track information by year of release for novels
* Still waiting patiently for graphs to output. Will it ever work?

## 7-11-19
* Work on latex writeup sheet
* Classification by genre:
	* TV
		* There are 570 pages in the current set.
		* Mean: 0.8982081157604296, Stdev: 0.05148345920514732
		* Drama:
			* dramatic (2.120), an (1.108), seriously (1.073), hdnet (1.053), italian (1.038), newscaster (1.038), louder (1.029), hispanics (1.029), produces (1.021), offbeat (1.021), urine (1.019), networks (1.019), inability (1.013), outraged (1.010), mya (1.010), abcfamily (1.008), part (1.007), teaming (1.006), vegetarian (1.005), aames (1.000), 
		* Comedy:
			* sitcome (0.273), comedymax (0.504), lorimar (0.840), portrayers (0.946), players (0.948), upbringing (0.959), hammering (0.969), showbiz (0.969), allan (0.975), atheist (0.979), headache (0.980), episodenumber (0.982), bp (0.982), once (0.985), thelma (0.991), werewolf (0.991), songwriter (0.992), herb (0.993), washburn (0.994), anderson (0.996), 
	* Films
		* Mean: 0.8791396583893055, Stdev: 0.018811691635572975
		* Drama:
			* dramafilm (8.083), melodramatic (2.280), dramatics (2.003), thrilling (1.582), informative (1.522), prisoners (1.445), feelin (1.390), siegmann (1.389), novelby (1.373), sandlers (1.339), actions (1.326), alchohol (1.325), formidable (1.278), dedicate (1.267), possibly (1.266), penner (1.265), kilmer (1.263), reigning (1.249), forbid (1.241), stevenson (1.236), 
		* Comedy: 
			* comentary (0.069), gaves (0.718), functional (0.731), sequence (0.744), rafelson (0.750), originall (0.751), ninotchka (0.752), abbreviated (0.774), doves (0.801), serio (0.805), canes (0.805), whomever (0.825), stand (0.827), parishioners (0.828), lolita (0.839), writting (0.840), uncritically (0.840), maitland (0.841), comically (0.841), lanigan (0.843)


* Meeting with Richard and Andrew
	* Wrapped with classification & feature identification
	* New metadata sheet: Collected times and visualized
	* Collected purity for graphs--still need to collect purity based on genre/period. However--only able to generate smaller graph. (where the purity of the set containing a majority of novels was 96.0%, the purity of the set containing a majority of films was 100.0%, and the purity of the set containing a majority television shows was 97.9%)
	* To-do
		* Remove typos, re-run classifier
		* Idea of contemporanean-ousness: How much do we care about recent vs. old. How does recent-ness
		* Anova: Compare the distribution of edit gaps for each set. Or, run a linear regression. Variable is edit time, genre is another variable. 
		* Is there a relationship between things that are highly edited and topic modeling the content of the edits? Take all of the edit histories as the documents, topic model it. Would it be useful to ask what the dominnat topics in the subset of documents that are higher than average? Topics that are common in higher-quartile debates vs. topics that are common in lower-quartile debates.
			* Regardless of genre/medium, people get really agitated about certain topics. 
			* Go through topic space, question: Is the expected probability of this topic higher in a high argument document than a low argument document? Is that topic overdiscussed in the argumentative edits?
				* Linear model using the topics, train on class, ignore medium.
	* General task list:
		* Topic model on the added words. Get it to the point where models are decent. Then, compare topic models for high-frequency and low-frequency edit pages
		* Classification sans-non-dictionary words
			* Currently classifying.
		* Run Louvain on graphs of just novels, just films, just TV. Purity of period & comedy/drama.
			* Graphs being generated.
		* Anova on time between edits, time between edits for different genres.

## 7-15-19
* Classification w/o non dictionary words (period-based)
	* Novels
		* Mean: 0.7631841892188138, Stdev: 0.020925321035356662
		* Top 20 features associated with second class
			* ween (2.428), scheduling (1.519), announcements (1.459), fantasies (1.450), positives (1.400), torched (1.352), turvy (1.350), harden (1.329), ailed (1.319), officials (1.303), entertains (1.276), graphically (1.241), wed (1.237), writhe (1.237), virtue (1.231), cabaret (1.216), synod (1.213), measly (1.211), adulterer (1.203), homeland (1.202)
		* Top 20 features associated with first class
			* pseudonyms (0.518), serials (0.593), illustrating (0.629), adapting (0.715), originate (0.744), reprints (0.789), spying (0.790), editor (0.800), swiftness (0.801), rulers (0.811), westerners (0.815), drugstores (0.823), repudiate (0.824), chickens (0.830), publishers (0.833), coping (0.841), scientific (0.843), stover (0.845), femme (0.845), adventuress (0.847), 
	* Films
		* Mean: 0.862151696408977, Stdev: 0.014104762877833188
		* Top 20 features associated with second class
			* engulfing (9.817), redirecting (3.171), devouring (2.970), externally (2.616), theatrics (2.085), festive (1.996), bulletproof (1.896), spoiling (1.567), erotically (1.548), sh (1.545), globetrotters (1.530), thrilling (1.497), furbelows (1.485), prostitutes (1.467), rocked (1.443), tomboy (1.417), cultists (1.371), heisting (1.364), lino (1.351), rotter (1.346)
		* Top 20 features associated with first class
			* silents (0.304), preserves (0.588), profitable (0.594), domesticated (0.600), melodramatic (0.611), beeswax (0.629), censured (0.658), twerp (0.690), survivor (0.694), codebooks (0.719), remainder (0.721), overheated (0.747), reelection (0.754), fecal (0.760), dome (0.764), smilingly (0.771), corporatism (0.771), crisply (0.787), congressman (0.790), printed (0.791), 
	* TV
		* Mean: 0.8199504247445367, Stdev: 0.04249829782247689
		* Top 20 features associated with second class
			* premieres (1.287), realizations (1.255), millions (1.200), fond (1.177), channeling (1.130), beep (1.124), follows (1.114), relative (1.114), comas (1.108), seconded (1.102), whim (1.094), defends (1.093), aardvarks (1.082), killed (1.078), anyhow (1.078), premiering (1.077), willful (1.076), islanders (1.066), lookalikes (1.066), beached (1.063)
		* Top 20 features associated with first class
			* runaways (0.732), starry (0.812), releasing (0.836), regularly (0.839), including (0.845), syndrome (0.845), programing (0.855), appears (0.867), chill (0.874), releases (0.882), yeast (0.894), hag (0.907), broadcasters (0.911), dusk (0.922), aardvark (0.924), answer (0.924), beck (0.928), policemen (0.931), fatherhood (0.934), seeped (0.937), 
* Classification w/o non dictionary words (medium)
	* Overall: Mean: 0.9426482597119149, Stdev: 0.008605810457008986
	* Films to TV:
		* Mean: 0.9664461232257725, Stdev: 0.007752191080533349
		* TV:
			* decadence (2.764), cancellation (2.119), redirecting (1.897), reruns (1.503), site (1.440), resale (1.435), revolvers (1.427), cancels (1.346), dirge (1.343), rancher (1.304), thirties (1.298), ling (1.287), lasting (1.270), lift (1.269), stubble (1.259), amazons (1.241), boldest (1.239), focusing (1.199), syndicating (1.191), premiering (1.190), 
			* ['decadence', 'cancellation', 'redirecting', 'reruns', 'site', 'resale', 'revolvers', 'cancels', 'dirge', 'rancher', 'thirties', 'ling', 'lasting', 'lift', 'stubble', 'amazons', 'boldest', 'focusing', 'syndicating', 'premiering']
			* [2.76404983210137, 2.118865058472081, 1.897479831730622, 1.5026545305187053, 1.4404368097317801, 1.4352792417023517, 1.4272326584920079, 1.346314693751077, 1.343261398727523, 1.304274275653715, 1.2976221295343022, 1.2865521456883375, 1.2700485301658988, 1.269127697647907, 1.2594735594216309, 1.2414392892607407, 1.2385221368085189, 1.1986753578987366, 1.1911077816928737, 1.1897673314940103]
		* Films:
			* bangs (0.631), silents (0.667), directing (0.686), festive (0.830), spoiling (0.890), rotter (0.896), tabor (0.898), republicanism (0.904), weaned (0.911), schemer (0.923), westerners (0.928), stars (0.929), romanticism (0.930), permeate (0.932), sales (0.933), picturing (0.941), screens (0.942), graphs (0.943), uncritically (0.945), mayhem (0.946), 
			* ['bangs' 'silents' 'directing' 'festive' 'spoiling' 'rotter' 'tabor' 'republicanism' 'weaned' 'schemer' 'westerners' 'stars' 'romanticism' 'permeate' 'sales' 'picturing' 'screens' 'graphs' 'uncritically' 'mayhem']
			* [0.63145485 0.66698333 0.68627306 0.83027401 0.89044487 0.89615456 0.89815731 0.90423777 0.91116638 0.92255944 0.92778575 0.92851317 0.93035368 0.93194971 0.93252857 0.94105771 0.94248522 0.94258303 0.945303   0.94644705]
	* Novels to TV:
		* Mean: 0.9521622008135588, Stdev: 0.01641698574928082
		* TV
			* redirecting (3.108), lasting (1.850), cancellation (1.670), rancher (1.576), stars (1.550), liveliest (1.370), cancels (1.338), premiering (1.240), direly (1.223), completely (1.221), productively (1.220), hostess (1.204), decadence (1.198), clearance (1.166), resale (1.161), variously (1.147), scheduling (1.143), starry (1.141), ling (1.141), producers (1.131), 
			* ['redirecting', 'lasting', 'cancellation', 'rancher', 'stars', 'liveliest', 'cancels', 'premiering', 'direly', 'completely', 'productively', 'hostess', 'decadence', 'clearance', 'resale', 'variously', 'scheduling', 'starry', 'ling', 'producers']
			* [3.1079289992611363, 1.8501638620370742, 1.670187273060794, 1.5762349553233745, 1.5496848668666865, 1.3704901089618173, 1.3377222593068456, 1.240263752404679, 1.2225144044677327, 1.220519378480947, 1.2197526542126063, 1.203600667345946, 1.1978228829005872, 1.1660019314542804, 1.160955891480099, 1.1469247240904248, 1.1429862719408277, 1.1413154764209132, 1.1410476549586288, 1.1311829127089514]
		* Novels
			* authoress (0.741), spoiling (0.786), publishers (0.786), novelettes (0.790), trimester (0.800), adapting (0.819), publishing (0.867), thrilling (0.867), booksellers (0.868), deli (0.880), harebrained (0.899), suicides (0.902), presser (0.917), paperboy (0.917), bookcase (0.923), novelty (0.923), deadening (0.931), arose (0.936), considerably (0.936), messages (0.937), 
			* ['authoress' 'spoiling' 'publishers' 'novelettes' 'trimester' 'adapting' 'publishing' 'thrilling' 'booksellers' 'deli' 'harebrained' 'suicides' 'presser' 'paperboy' 'bookcase' 'novelty' 'deadening' 'arose' 'considerably' 'messages']
			* [0.74128964 0.78578178 0.78594201 0.78968193 0.79966483 0.81921846 0.86666624 0.86748227 0.86845459 0.87998313 0.89942833 0.90207838 0.916555   0.91689169 0.92278518 0.92315119 0.9312909  0.93556366 0.93576545 0.93743765]
	* Films to Novels:
		* Mean: 0.9328961193696145, Stdev: 0.01416047913308977
		* Novels
			* finality (2.566), publishing (2.496), repudiate (2.096), harden (1.848), serials (1.762), reprints (1.705), beta (1.655), bestselling (1.570), locusts (1.567), illustrating (1.497), torched (1.397), prosecute (1.382), publishers (1.351), reciprocal (1.347), novelization (1.331), novelty (1.309), omnipotence (1.305), nebulous (1.282), paperboy (1.275), sordidness (1.267), 
			* ['finality', 'publishing', 'repudiate', 'harden', 'serials', 'reprints', 'beta', 'bestselling', 'locusts', 'illustrating', 'torched', 'prosecute', 'publishers', 'reciprocal', 'novelization', 'novelty', 'omnipotence', 'nebulous', 'paperboy', 'sordidness']
			* [2.5664731593211343, 2.49640351306586, 2.095546996011784, 1.8482320857992942, 1.7623965134421526, 1.7047343847270022, 1.654915145929004, 1.5703582888111776, 1.5666564064517263, 1.496952924770237, 1.3971756618907292, 1.3815112373914709, 1.3508147469400362, 1.346996182736741, 1.3314103484559785, 1.309248466535026, 1.3053213192227222, 1.2822997359475334, 1.2748944075353712, 1.2671984061162538]
		* Films
			* silents (0.506), forcing (0.520), archives (0.558), stars (0.627), temples (0.637), redirecting (0.638), directing (0.640), billet (0.698), monograph (0.705), melodramatic (0.714), dramatic (0.726), beeswax (0.737), mayhem (0.739), distributes (0.740), digresses (0.767), comer (0.781), uncritically (0.784), westerners (0.787), documented (0.795), tomboy (0.798), 
			* ['silents' 'forcing' 'archives' 'stars' 'temples' 'redirecting' 'directing' 'billet' 'monograph' 'melodramatic' 'dramatic' 'beeswax' 'mayhem' 'distributes' 'digresses' 'comer' 'uncritically' 'westerners' 'documented' 'tomboy']
			* [0.50574122 0.52019373 0.5575963  0.62749173 0.63686028 0.6380436 0.64046032 0.69754947 0.70528804 0.7138444  0.72634524 0.73689103 0.73927931 0.74049792 0.76722557 0.78105616 0.78380561 0.78720273 0.7950537  0.798314  ]

* Purity tests on TV graph:
	* Using only comedy and drama, 3 largest sets:
		* Purity of comedy set is 77.7%, its size is 381.
		* Purity of comedy set is 57.1%, its size is 112.
		* Purity of comedy set is 80.8%, its size is 78.
	* Using all genres, 3 largest sets:
		* Purity of comedy set is 29.4%, its size is 1007.
		* Purity of comedy set is 14.6%, its size is 438.
		* Purity of comedy set is 14.1%, its size is 446.

## 7-16-19
* optimize graph creation using numpy lists so that is actually works.
	* fix recursion error to generate graphs for films & everything
	* optimize graph creation algorithm
* add average times without longer edits as metadata column (for ANOVA)
	* something is wrong, box plot is all negative

## 7-17-19
* Continue work on Latex doc
* Consolidate information on distinguishing features

## 7-18-19
* These darn graphs still aren't working. Switch to random sampling using sets of 300 pages from each. Generate 50 graphs for just novels, films (each representing 300 pages) and 25 for tv (representing 300 pages) and everything (representing 900 pages)
* Haha! I did it. Fuck you, world.

* tv (50 graphs each representing 300 random articles)
	* Genre (only counting nodes tagged as drama or comedy)
		* Average purity: 0.7638609717314676
		* Stdev.: 0.05022413649468192
		* Clusters with more than 50 nodes: 17
		* Number of clusters that were majority [genre]: {'comedy': 17}
	* Period (based on median for all works)
		* Average purity: 0.7081603777061096
		* Stdev.: 0.11200074514214772
		* Clusters with more than 50 nodes: 140
		* Number of clusters that were majority [period]: {Early: 85, Late: 55}
	* Total clusters: 354

* films (50 graphs each representing 300 random articles)
	* Genre (only counting nodes tagged as drama or comedy)
		* Average purity: 0.5752360339319412
		* Stdev.: 0.05636836933692584
		* Clusters with more than 50 nodes: 49
		* Number of clusters that were majority [genre]: {'drama': 44, 'comedy': 5}
	* Period (based on median for all works)
		* Average purity: 0.7845490518778967
		* Stdev.: 0.09235097922452261
		* Groups with more than 50 nodes: 106
		* Number of clusters that were majority [period]: {Early: 53, Late: 53}
	* Total clusters: 232

* novels (50 graphs each representing 300 random articles)
	* Period
		* Average purity: 0.5788789960579163
		* Stdev.: 0.06429547474760233
		* Clusters with more than 50 nodes: 155
		* Number of clusters that were majority [period]: {Early: 113, Late: 42}
	* Total clusters: 241

* all genres (50 graphs each representing 300 random articles)
	* Average purity: 0.9246741671740376
	* Stdev.: 0.05279507784365967
	* Clusters with more than 50 nodes: 151
	* Number of clusters that were majority [medium]: {'films': 50, 'novels': 50, 'tv': 51}
	* Total clusters: 316

## 7-19-19
* Classification by genre
* Films
	* There are 9370 pages in the current set.
	* Mean: 0.884407901514087, Stdev: 0.01851011652354421
	* Dramas 
		* dramatic (7.431), melodramatic (2.359), dramatics (2.055), reigning (2.018), thrilling (1.727), feelings (1.497), informative (1.473), novelist (1.429), prisoners (1.404), activate (1.378), formidable (1.369), lovesick (1.321), gibbon (1.275), holes (1.259), possum (1.259), pennies (1.248), wardens (1.238), understandably (1.229), someplace (1.228), wellbeing (1.226), 
		* ['dramatic', 'melodramatic', 'dramatics', 'reigning', 'thrilling', 'feelings', 'informative', 'novelist', 'prisoners', 'activate', 'formidable', 'lovesick', 'gibbon', 'holes', 'possum', 'pennies', 'wardens', 'understandably', 'someplace', 'wellbeing']
		* [7.431364095063198, 2.358985152899935, 2.0549447892946975, 2.0177899620019546, 1.7271985670368677, 1.4967392894215623, 1.4733650505770504, 1.4291630023489927, 1.4038980673084624, 1.3784717739112333, 1.368838422256153, 1.3213879830041833, 1.2753126366169227, 1.2590047188223272, 1.2589660233211764, 1.2481365531637727, 1.2382714297221826, 1.2288936875408185, 1.2277200654802052, 1.2257942399245632]

	* Comedies
		* comer (0.077), tickle (0.514), gawker (0.678), sequence (0.690), functional (0.714), nip (0.734), canes (0.739), superb (0.742), originally (0.765), harebrained (0.789), opposed (0.792), reinforced (0.796), watery (0.815), heroic (0.818), manslaughter (0.821), serious (0.825), doves (0.826), thirds (0.832), turning (0.832), convincingly (0.837), 
		* ['comer' 'tickle' 'gawker' 'sequence' 'functional' 'nip' 'canes' 'superb', 'originally' 'harebrained' 'opposed' 'reinforced' 'watery' 'heroic' 'manslaughter' 'serious' 'doves' 'thirds' 'turning' 'convincingly']
		* [0.07650343 0.514035   0.67832333 0.6896141  0.71440496 0.73440707 0.73923598 0.74236464 0.76510716 0.78859294 0.79246313 0.795933 0.81466733 0.81752191 0.82054541 0.82505895 0.82594696 0.83186016 0.83242587 0.8371477 ]

* TV
	* Mean: 0.8892627340686413, Stdev: 0.06488349319067703
	* Dramas

	* Comedies
		* site (0.268), comers (0.571), upbringing (0.947), filming (0.948), youngest (0.953), players (0.956), allegations (0.959), hammering (0.963), west (0.966), showcase (0.968), songwriter (0.970), episodic (0.971), brace (0.975), one (0.982), frontier (0.984), hind (0.984), washed (0.984), sheen (0.987), headache (0.988), them (0.988), 
		* ['site' 'comers' 'upbringing' 'filming' 'youngest' 'players' 'allegations' 'hammering' 'west' 'showcase' 'songwriter' 'episodic' 'brace' 'one' 'frontier' 'hind' 'washed' 'sheen' 'headache' 'them']
		* [0.2680163  0.57050474 0.94730643 0.9481638  0.95319314 0.9561723 0.95928647 0.96287544 0.9657273  0.96844824 0.97027206 0.97114024 0.97549044 0.98161194 0.98387711 0.98428408 0.98432136 0.98660535 0.98782596 0.98786517]
* Tukey
	* Average time overall
		 Multiple Comparison of Means - Tukey HSD,FWER=0.05
		===================================================
		group1 group2  meandiff   lower      upper   reject
		---------------------------------------------------
		films  novels  311.8257  241.0769   382.5744  True 
		films    tv   -575.2783 -716.4065  -434.1501  True 
		novels   tv    -887.104 -1035.1849  -739.023  True 
	* Average time short
		Multiple Comparison of Means - Tukey HSD,FWER=0.05
		===============================================
		group1 group2 meandiff  lower    upper   reject
		-----------------------------------------------
		films  novels -4.4329  -6.1771  -2.6886   True 
		films    tv   -24.725  -28.2389 -21.2111  True 
		novels   tv   -20.2921 -23.9733 -16.6109  True 
		-----------------------------------------------

* 7-22-19
* ANOVA in R: 
	* Every edit
		              Diff   Lower CI  Upper CI
	novels-films  311.8257   248.8543  374.7970
	tv-films     -575.2783  -804.9320 -345.6246
	tv-novels    -887.1040 -1119.1615 -655.0464

	* Edits of less than one month only
	                   Diff   Lower CI   Upper CI
	novels-films  -4.432879  -6.128183  -2.737576
	tv-films     -24.725003 -27.939024 -21.510982
	tv-novels    -20.292124 -23.648979 -16.935268

* 7-23-19
	* Work on presentation
	* Generate metadata visuals

* 7-24-19
* Years with the highest average edits

325  1960  1154.900000      tv
108  2009  1180.143564   films
328  1963  1197.636364      tv
321  1956  1199.714286      tv
144  1850  1215.000000  novels
330  1965  1221.555556      tv
377  2012  1262.766667      tv
380  2015  1274.296296      tv
368  2003  1287.338983      tv
107  2008  1298.235602   films
361  1996  1314.026316      tv
362  1997  1349.514286      tv
365  2000  1369.526316      tv
371  2006  1409.246154      tv
367  2002  1450.838710      tv
374  2009  1489.876712      tv
375  2010  1499.711864      tv
359  1994  1511.531250      tv
122  1826  1513.000000  novels
378  2013  1523.136364      tv
354  1989  1540.880000      tv
376  2011  1544.259259      tv
366  2001  1547.607143      tv
373  2008  1737.918367      tv
370  2005  1829.014925      tv
372  2007  1854.869565      tv
369  2004  2049.120000      tv
358  1993  2259.666667      tv
364  1999  2571.239130      tv
145  1851  3152.500000  novels

## 7-25-19
* Presentations
	* Be sure to add global stats!
	* 

Average edits
	* films :  235.9300390117035
	* novels :  122.96153046371387
	* tv :  1216.2775423728813

Early novels tend to be very confined to genre: the adventure, the western, the femme, etc. Late novels are broader in definition, less bound by genre-words.

Novels and films shift towards more sexual and physical descriptors over time


Late period television tends to be more aggressive and twisty, early is family and work related

Notes
* Take the sum of edits in the 5 years after release.
	* control for that window. Is more recent stuff getting less attention?
	* Test edits from start date of page
* Take the three largest clusters from run instead of >50
* Confusion matrix representation
* Words unique to novels compared to the two other mdeia combined
* TV vs Film, novels vs. visual. Use topic modeling. Features that have the most discriminatory power. Increments of 25 for k value. 

* Next steps
	* Edits from 2000-2005 compared to edits from 2005-2010.
		* Compare changes over 5-year windows by.
		* Are edits being driven by user differences, world events?
		* NEXT STEP
		* Switch over entirely to topic modeling.
		* Find more hypothesis to test for.
	* Which cultural domains have higher levels of cultural activity?
		* More comparison points to think about.
		* Start scaling up! Look into other cultural domains. 
	* Graphs: Expand sampling procedure to 1k graphs instead of 50.
	* Number of edits per user & distribution


## 10-7-19
* Generate 1,000 graphs for each space.
* Meeting w/ all. Discuss continuing project.

## 9-4-19
* Previewed metadata sheets for sciences, sports, politics.
* For two weeks: Prepare slides reviewing summary stats for each domain. Average words per article, etc.