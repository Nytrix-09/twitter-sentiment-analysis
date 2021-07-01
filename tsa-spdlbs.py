import tweepy,csv,re
from textblob import TextBlob
import matplotlib.pyplot as plt
# text=TextBlob("This is a sample text")
# ans=text.sentiment.polarity
class SentimentAnalysis:
    def __init__(self):
        self.tweets=[]
        self.tweetText=[]

    def DownloadData(self):
        #login into twitter
        #post login to twitter account, apply for a developer account with twitter and then you will have the credentials to enter below
        ConsumerKey = ''
        ConsumerKeySecret = ''
        AccessToken = ''
        AccessTokenSecret = ''
        auth=tweepy.OAuthHandler(ConsumerKey,ConsumerKeySecret)
        auth.set_access_token(AccessToken,AccessTokenSecret)
        
        api=tweepy.API(auth)

        #User Input here
        SearchTerm= input("Enter key word: ")
        NoOfTweets=int(input("Enter number of tweets: "))

        #Search Tweets (tweepy command)
        self.tweets=tweepy.Cursor(api.search, q = SearchTerm, lang="en").items(NoOfTweets)

        #File handling, here it makes a "twitter_data.csv" file and writes the result in the file 
        csvfile=open('twitter_data.csv','a')
        csvwriter=csv.writer(csvfile)
        
        #Defining Paramaters that will help classify tweet sentiment 
        neutral=0
        weakly_positive=0
        moderately_positive=0
        strongly_positive=0
        weakly_negative=0
        moderately_negative=0
        strongly_negative=0

        for tweet in self.tweets:
            self.tweetText.append(self.cleanText(tweet.text).encode('utf-8'))
            analysis=TextBlob(tweet.text)
            polarity=analysis.sentiment.polarity
            polarity+=polarity
            
            #condition for neutral tweet sentiment
            if (analysis.sentiment.polarity==0):
                neutral+=1
            #condition for weakly positive tweet sentiment
            elif (analysis.sentiment.polarity>0 and analysis.sentiment.polarity<=0.3):
                weakly_positive+=1
            #condition for moderately tweet sentiment
            elif (analysis.sentiment.polarity>0.3 and analysis.sentiment.polarity<=0.6):
                moderately_positive+=1
            #condition for strongly positive tweet sentiment
            elif (analysis.sentiment.polarity>0.6 and analysis.sentiment.polarity<=1):
                strongly_positive+=1
            #condition for weakly neagtive tweet sentiment
            elif (analysis.sentiment.polarity>=-0.3 and analysis.sentiment.polarity<0):
                weakly_negative+=1
            #condition for moderately negative tweet sentiment
            elif (analysis.sentiment.polarity>=-0.6 and analysis.sentiment.polarity<-0.3):
                moderately_negative+=1
            #condition for strongly negative tweet sentiment
            elif (analysis.sentiment.polarity>=-1 and analysis.sentiment.polarity<-0.6):
                strongly_negative+=1
        
        #Closing the file after writing
        csvwriter.writerow(self.tweetText)
        csvfile.close()   

        #Calculating percentage of each type of tweet sentiment for the focus keyword
        neutral= self.percentage(neutral, NoOfTweets)
        weakly_positive=self.percentage(weakly_positive, NoOfTweets)
        moderately_positive=self.percentage(moderately_positive, NoOfTweets)
        strongly_positive=self.percentage(strongly_positive, NoOfTweets)
        weakly_negative=self.percentage(weakly_negative, NoOfTweets)
        moderately_negative=self.percentage(moderately_negative, NoOfTweets)
        strongly_negative=self.percentage(strongly_negative, NoOfTweets)

        polarity=polarity/NoOfTweets

        if(polarity==0):
            print("Neutral")
        elif (polarity>0 and polarity<=0.3):
            print("Weakly Positive")
        elif (polarity>0.3 and polarity<=0.6):
            print("Moderately Positive")
        elif (polarity>0.6 and polarity<=1):
            print("Strongly Positive")
        elif (polarity>=-0.3 and polarity<0):
            print("Weakly Negative")
        elif (polarity>=-0.6 and polarity<-0.3):
            print("Moderately Negative")
        elif (polarity>=-1 and polarity<-0.6):
            print("Strongly Negative")
        
        #Report with plain Numerical Values
        print("\n\n Report With Values: ======> ")

        print(str(neutral)+" % people are neutral")
        print(str(weakly_positive)+" % people are weakly_positive")
        print(str(moderately_positive)+" % people are moderately_positive")
        print(str(strongly_positive)+" % people are strongly_positive")
        print(str(weakly_negative)+" % people are weakly_negative")
        print(str(moderately_negative)+" % people are moderately_negative")
        print(str(strongly_negative)+" % people are strongly_negative")
        
        #Plotting by calling the plotPieChart() class after the result of the focus keyword's sentiment is output.
        self.plotPieChart(neutral,weakly_positive,moderately_positive,strongly_positive,weakly_negative,moderately_negative,strongly_negative,SearchTerm,NoOfTweets)


    #To clean the focus keyword input by the user 
    def cleanText(self,tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+) | ([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)"," ",tweet).split()) #all characters starting with capital, small or with numbers and even links will be accessed

    #To calculate the percentage of each sentiment found for the keyword 
    def percentage(self,part,total):
        count=100 * float(part)/float(total)
        return format(count,'.2f')

    #Defining pie chart class and how plotting is carried out with their colors etc.
    def plotPieChart(self,neutral,weakly_positive,moderately_positive,strongly_positive,weakly_negative,moderately_negative,strongly_negative,SearchTerm,NoOfTweets):
        labels= [
            "neutral "+str(neutral)+" %",
            "weakly_positive "+str(weakly_positive)+" %",
            "moderately_positive "+str(moderately_positive)+" %",
            "strongly_positive "+str(strongly_positive)+" %",
            "weakly_negative "+str(weakly_negative)+" %",
            "moderately_negative "+str(moderately_negative)+" %",
            "strongly_negative "+str(strongly_negative)+" %",
        ]

        sizes = [
            neutral,weakly_positive,moderately_positive,strongly_positive,weakly_negative,moderately_negative,strongly_negative
        ]

        colors = [
            "gold",
            "lightgreen",
            "yellowgreen",
            "darkgreen",
            "lightsalmon",
            "red",
            "darkred"
        ]

        patches, texts = plt.pie(sizes,colors=colors,startangle=90)
        plt.legend(patches,labels,loc="best")
        plt.title("People reaction in "+str(SearchTerm)+" by analysing "+str(NoOfTweets)+" Tweets.")
        plt.axis("equal")
        plt.tight_layout()
        plt.show()

#Main to run the program
if __name__ == "__main__":
    sa=SentimentAnalysis()
    sa.DownloadData()
