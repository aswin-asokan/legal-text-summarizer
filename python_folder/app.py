import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the pre-trained T5 tokenizer and model
model_name = "t5-base"  # Or you can use "t5-base" or "t5-large" for better performance
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

def summarize_text(text):
    """
    Summarize the given legal text using the T5 model.
    
    Parameters:
    - text (str): The legal text to be summarized.
    
    Returns:
    - str: The summarized text.
    """
    # Preprocess the text
    input_text = "summarize: " + text
    inputs = tokenizer(input_text, return_tensors="pt", max_length=512, truncation=True, padding=True)

    # Generate the summary
    summary_ids = model.generate(inputs["input_ids"], max_length=150, num_beams=4, early_stopping=True)

    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

# Example legal text
legal_text = """
Appeal No.84 of 1960. 888 Appeal from the judgment and decree dated July 26, 1956. of the Bombay, High Court in Appeal No. he 138 of 1956. The appellant in person. B. R. L. Ayengar and D. Gupta, for the respondent. April 12. The Judgment of the Court was delivered by SINHA, C. J. The main question for decision in this appeal, on a certificate of fitness granted by the ' High Court of Judicature at Bombay, is whether a public servant, who has been officiating in a higher post but has been reverted to his substantive rank as a result of an adverse finding against him in a departmental enquiry for misconduct, can be said to have been reduced in rank within the meaning of section 240(3) of the Government of India Act, 1935. The learned Civil Judge, Senior Division, by his, Judgment and Decree dated October 31, 1955, held that it was so. The High Court of Bombay, on a first appeal from that decision, by its Judgment and Decree dated July 26, 1956, has held to the contrary. In so far as it is necessary for the determination of this appeal, the facts of this case may shortly be stated as follows. The appellant was holding the rank of a Mamlatdar in the First Grade and Was officiating as a District Deputy Collector. In the latter capacity he was functioning as a District Supplies Officer. He had to undertake tours in the discharge of his official duties for which he maintained a motor car. In respect of one of his travelling allowance bills, it was found that he had charged travelling allowance in respect of 59 miles whereas the correct distance was only 51 miles. A departmental enquiry was held against him as a result of which he was reverted to his original rank as Mamlatdar, by virtue of the Order of the Government dated August 11, 1948, (exhibit 35), which was to the following effect: "After careful consideration Government have decided to revert you to Mamlatdar for a period of 889 three years and have further directed that you should refund the excess mileage drawn by you in respect of the three journeys. " The appellant made a number of representations to the Government challenging the correctness of the findings against him and praying for re consideration of the Order of Reversion passed against, him but to no effect, in spite of the fact that ultimately the Accountant General gave his opinion that the appellant had not overcharged and that there was no fraud involved in the travelling allowance bill which was the subject matter of the charge against him. But ultimately, by a Notification date& March 26, 1951, (exhibit 61), the appellant was promoted to the Selection Grade with effect from August 1, 1950, but even so the Order of Reversion passed against the appellant remained effective and appears to have affected his place in the Selection Grade. Eventually, the appellant retired from service on superannuation with effect from November 28, 1953. He filed his suit against the State of Bombay on August 2, 1954, for a declaration that the Order of the Government dated August 11, 1948, was void, inoperative, wrongful, illegal and ultra vires, and for recovery of Rs. 12,866 odd or account of his arrears of salary, allowances, etc. with interest and future interest. The learned Civil Judge Senior Division, at Belgaum, came to the conclusion that the first part of the departmental enquiry held against the plaintiff leading up to the findings against him was free from any defect but that he had no been given the opportunity of showing cause against the punishment proposed to be inflicted upon him a a result of those findings, in so far as no show cause notice was given to him nor a copy of the enquire, report showing the grounds on which the findings ha, been based. There was, thus, according to the finding of the Trial Court, no full compliance with the requirements of section 240(3) of the Government of India Act 1935. The Court also held that the Order of Reversion amounted to a penalty imposed upon the plaintiff as a result of the enquiry. The Court, therefore, cam 890 to the conclusion that the Order aforesaid passed by the Government reverting him to the substantive rank was void and granted him that declaration, but dismissed his suit, with costs, in respect of the arrears Claimed by him as aforesaid on the ground that it was based on tort and not on contract. There was an appeal by the plaintiff in respect of the dismissal of his claim for arrears, and cross objections by the State in respect of that part of the judgment and decree which had granted declaration in favour of the plaintiff. The High Court dismissed the appeal by the plaintiff and allowed the cross objections of the de fendant respondent in respect of the declaration, but made no orders as to the costs of the appeal and the cross objections. The High Court held that the Order of Reversion, even assuming that it was a punishment as a result of the departmental enquiry against the appellant, was not a punishment within the meaning of section 240(3) of the Government of India Act, 1935. It also held that the Order of Reversion was not a punishment at all. In this Court, the appellant, who has argued his own case with ability, has urged in the first place, and in our opinion rightly, that his case is covered by the observations of this Court in Parshotam Lal Dhingra vs Union of Indid (1). Those observations are as follows: "A reduction in rank likewise may be by way of punishment or it may be an innocuous thing. If the Government servant has a right to a particular rank, then the very reduction from that rank will operate as a penalty, for he will then lose the emoluments and privileges of that rank. If, however, he has no right to the particular rank, his reduction from an officiating higher rank to his substantive lower rank will not ordinarily be a punishment. But the mere fact that the servant has no title to the post or the rank and the Government has, by contract, express or implied, or under the rules, the right to reduce him to a lower post does not mean that an order of reduction of a servant to a lower (1) , 863 64. 891 post or rank cannot in any circumstances be a punishment. The real test for determining whether the reduction in such cases is or is not by way of punishment is to find out if the order for the reduction also visits the servant with any penal consequences. Thus if the order entails or provides for the forfeiture of his pay or allowances or the loss of his seniority in his substantive rank or the stoppage or postponement of his future chances of promotion, then that circumstance may indicate that although in form the Government had purported to exercise its right to terminate the employment or to reduce the servant to a lower rank under the terms of the contract of employment or under the rules, in truth and reality the Government has terminated the employment as and by way of penalty. The use of the expression "termi nate" or "discharge" is not conclusive. Tn spite of the use of such innocuous expressions, the court has to apply the two tests mentioned above, namely, (1) whether the servant bad a right to the post or the rank or (2) whether he ha,,; been visited with evil consequences of the kind hereinbefore referred to? If the case satisfies either of the two tests then it must be held that the servant has been punished and the termination of his service must be taken as a dismissal or removal from service or the reversion to his substantive rank must be regarded as a reduction in rank and if the requirements of rules and article 311, which give protection to Government servant have not been complied with, the termination of the service or the reduction in rank must be held to be wrongful and in violation of the consti tutional right of the servant. " He has rightly pointed out that he would have continued as a Deputy Collector but for the Order of the Government, dated August 11, 1948, impugned in this case, as a result of the enquiry held against him, and that his reversion was not as a matter of course or for administrative convenience. The Order, in terms, held him back for three years. Thus his emoluments, present as well as future, were adversely affected by the 892 Order aforesaid of the Government. In the ordinary course, he would have continued as a Deputy Collector with all the emoluments of the post and would have been entitled to further promotion but for the setback in his service as a result of the adverse finding against him, which finding was ultimately declared by the Account ant General to have been under a misapprehension of the true facts. It is true that he was promoted as a result of the Government Order dated March 26, 1951, with effect from August 1, 1950. B ' that promotion did not entirely cover the ground lost by him as a result of the Government Order impugned in this case. It is noteworthy that the Judgment of the High Court under appeal was given in July, 1956, when the decision of this Court in Dhingra 's case (1) had not been given. The decision of this Court was given in November, 1957. Of the two tests laid down by this Court, certainly the second test applies, if not also the first one. He may or may not have a right to hold the post or the rank, but there is no doubt that he was visited with evil consequences. Ordinarily, if a public servant has been officiating in a higher rank it cannot be said that he has a substantive right to that higher rank. He may have to revert to his substantive rank as a result of the exigencies of the service or he may be reverted as a result of an adverse finding in an enquiry against him for misconduct. In every case of reversion from an officiating higher post to his substantive post, the civil servant concerned is deprived of the emoluments of the higher post. But that cannot, by itself, be a ground for holding that the second test in Dhingra 's case (1), namely, whether he has been visited with evil consequences, can be said to have been satisfied. Hence, mere deprivation of higher emoluments as a consequence of a reversion cannot amount to the "evil consequences" referred to in the second test in Dhingra 's case (1); they must mean something more than mere deprivation of higher emoluments. That being so, they include, for example, forfeiture of substantive pay, loss of seniority, etc. Applying that (1) [1058] S.C.P. 326, 863 64. 893 test to the present case, it cannot be said that simply because the appellant did not get a Deputy Collector 's salary for three years, he was visited with evil conse quences of the type contemplated in Dhingra 's case (1). Even if he had been reverted in the ordinary course of the exigencies of the service, the same consequences would have ensued. If the logs of the emoluments attaching to the higher rank in which he was officiating was the only consequence of his reversion as a result of the enquiry against him, the appellant would ' have no cause of action. But it is clear that as a result of the Order dated August 11, 1948 (exhibit 35), the appellant lost his seniority as a Mamlatdar, which was his substantive post: That being so, it was not a simple case of reversion with no evil consequences; it had such consequences as would come within the test of punishment as laid down in Dhingra 's case. If the reversion had not been for a period of three years, it could not be said that the appellant had been punished within the meaning of the rule laid down in Dhingra 's case, (1). It cannot be asserted that his reversion to a substantive post for a period of three years was not by way of punishment. From the facts of this case it is clear that the appellant was on the upward move in the cadre of his service and but for this aberration in his progress to a higher post, he would have, in ordinary course, been promoted as he actually was sometime later when the authorities realised perhaps that he had not been justly treated, as is clear from the Order of the Government, dated March 26, 1951, promoting him to the higher rank with effect from August 1, 1950. But that belated justice meted out to him by the Government did not completely undo the mischief of the Order of Reversion impugned in this case. It is clear to us, therefore, that as a result of the Order of Reversion aforesaid, the appellant had been punished and that the Order of the Government punishing him was not wholly regular. It has been found that the requirements of section 240(3) of the Government of India Act, 1935, corresponding to article 311 (2) of the Constitution, had not been fully complied with. His (1) ,863 64. 894 reversion in rank, therefore, was in violation of the Constitutional guarantee. In view of these considerations it must be held that the High Court was not right in holding against the appellant that his reversion was not a punishment contemplated by section 240(3) of the Government of India Act, 1935. On this part of the case, in our opinion, the decision of the High part has to be reversed and that of the Trial Court hat his reversion to his substantive rank was void, must be restored. The question then arises whether he is entitled to any relief in respect of his claim for arrears of salary and dearness allowance. He has claimed Rs. 10,777 odd as arrears of pay, Rs. 951 odd as arrears of dearness allowance, as also Rs. 688 odd as arrears of daily allowance plus interest of Rs. 471 odd, thus aggregating to the sum of Rs. 12,886 odd. This claim is spread over the period August, 1946, to November, 1953, that is to say, until the date of his retirement from Government service, plus future interest also. On this part of the case the learned Trial Judge, relying upon the case of the High Commissioner for India and Pakistan vs I. M. Lall (1) held that a government servant has no right to recover arrears of pay by an action in a Civil Court. He got over the decision of this Court in the State of Bihar vs Abdul Majid (2) on the ground that that case has made a distinction between a claim based on a contract and that on a tort. In the instant case, he came to the conclusion that as the plaintiff had claimed the difference between the pay and allowance actually drawn and those to which he would have been entitled but for the wrongful orders, the claim was based on tort and, therefore, the plaintiff was not entitled to any relief. On the question of limitation, he held that the suit would be governed by article 102 of the Indian Limitation Act (IX of 1908) as laid down by the Federal Court in the case of The Punjab Province vs Pandit Tarachand (3). In that view of the matter, the learned Judge held that adding the period of two months of the statutory notice under section 80 of the Code of Civil Procedure given to (1) (1948) L.R. 75 I.A. 225. (2) ; (3) 895 Government, the claim would be in time from June 2, 1951. Hence the Trial Court, while giving the declaration that the Order impugned was void, dismissed, the rest of the claim with a direction that the plaintiff was to pay 3/4ths of the costs of the suit to the defendant. The High Court dismissed the suit in its entirety after allowing the cross objections of the State. The appellant contended that his suit for arrears of salary would not be governed by the three years rule laid down in article 102 of the Limitation Act and that the decision of the Federal Court in Tarachand 's case (1) was not correct. The sole ground on which this contention was based was that "salary" was not included within the term "wages". In our opinion, no good reasons have been adduced before us for not following the aforesaid decision of the Federal Court. In the result, the appeal is allowed in part, that is to say, the declaration granted by the Trial Court that the Order of the Government impugned in this case is void, is restored, in disagreement with the decision of the High Court. The claim as regards arrears of salary and allowance is allowed in part only from the 2nd of June, 1951, until the date of the plaintiff 's retirement from Government service. There will be no decree for interest before the date of the suit, but the decretal sum shall bear interest at 6% per annum from the date of the suit until realisation. The plaintiff appellant will be entitled to three fourths of his costs throughout, in view of the fact that his entire claim is not being allowed. Appeal allowed in part.
"""

# Generate the summary (or label) for the legal text
summary = summarize_text(legal_text)

# Print the summary (the predicted label or category)
print("Summary/Prediction:", summary)
