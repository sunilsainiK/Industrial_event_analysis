#  Sentimental_Analysis

__This is frequency based model__

 We can use following technique to analyze

 __Naive Bayes Classifier__

   P(A|B) = P(B|A)P(A)/P(B)

   We’ll represent events by a Bag of Words, which is a set of features “the word appears f times” for each word w in the sentence and f, the frequency of w in the sentence. Assuming the Naive Bayes assumption that these features are independent, this formula helps us deduce the probability that the events is Normal (A) knowing that w appears f times (B) for every w. In fact, we can deduce from the frequencies in a large enough dataset the probability for a sentence to be Normal (A), and the probabilities of every feature and then of their intersection (B).

 __Rule-based sentiment models__

   To improve the Naive Bayes methods and make it fits the short sentences sentiment analysis challenge, we added some rules to take into account negations, intensity markers nuance, and other semantic structures that appear very often near sentimental phrases and change their Behaviours.
