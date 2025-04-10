import torch
import re
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from nltk.tokenize import sent_tokenize
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load models
model_path = "/home/aswin/Documents/BERT Summarisation/python_folder/bert_caselawbert"
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

grammar_model_name = "vennify/t5-base-grammar-correction"
grammar_tokenizer = T5Tokenizer.from_pretrained(grammar_model_name, legacy=False)
grammar_model = T5ForConditionalGeneration.from_pretrained(grammar_model_name)

model.eval()

# Label Mapping
label_map = {"FACTS": 0, "ARGUMENT": 1, "ANALYSIS": 2, "JUDGMENT": 3, "STATUTE": 4, "O": 5}
id_to_label = {v: k for k, v in label_map.items()} 

# Custom Sentence Tokenization
def custom_sent_tokenize(text):
    # Preserve formatting for statutes, legal abbreviations, and honorifics
    text = re.sub(r"\bNo\.\s*(\d+)", r"Number_\1", text)  
    text = re.sub(r"\b(\d{1,2})[./](\d{1,2})[./](\d{4})\b", r"DATE_\1_\2_\3", text)  
    text = re.sub(r"(^|\s)(\d+\.\s*){2,}", " ", text)  
    text = re.sub(r"(Section\s\d+(\s*\(\w+\))?)", r"§\1§", text)  
    text = re.sub(r"\b(N\.I\.|I\.P\.C\.|C\.R\.P\.C\.|Act\.)", r"§\1§", text)  
    text = re.sub(r"\b(Dr|Mr|Mrs|Ms|Prof|Sr|Smt|Jr|Col|Gen|Lt|Maj|Hon|Rev|St)\.", r"§\1§", text)  

    # Tokenization
    sentences = sent_tokenize(text)

    # Restore original format
    sentences = [s.replace("§", "").replace("Number_", "No. ").replace("DATE_", "") for s in sentences]  
    return sentences

# Function to extract Rs. values
def extract_money(text):
    pattern = r"Rs\.?\s*\d+(?:,\d{3})*(?:\.\d+)?" 
    return re.findall(pattern, text)

# Function to correct grammar and reduce redundancy
def correct_grammar(text):
    input_text = "grammar: " + text  # Use "grammar" prompt instead of "rephrase"
    input_ids = grammar_tokenizer(input_text, return_tensors="pt").input_ids

    outputs = grammar_model.generate(input_ids, max_length=512)
    corrected_text = grammar_tokenizer.decode(outputs[0], skip_special_tokens=True)

    return corrected_text


# Function to summarize text and remove redundancy
def summarize_text(text):
    sentences = custom_sent_tokenize(text)  
    structured_summary = {label: [] for label in label_map.keys()}

    for sentence in sentences:
        inputs = tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)

        with torch.no_grad():
            outputs = model(**inputs)

        predicted_label = torch.argmax(outputs.logits, dim=1).item()
        label_name = id_to_label.get(predicted_label, "O")  

        if label_name == "STATUTE":
            if not re.search(r"\b(Section|Article|Act)\s+\d+", sentence):
                continue  

        if label_name != "O":  # Only keep meaningful sentences
            corrected_sentence = correct_grammar(sentence)  # Grammar fix without rephrasing
            structured_summary[label_name].append(corrected_sentence)

    # Convert structured summary to readable text format
    summary_text = ""
    for label, sentences in structured_summary.items():
        if sentences:  # Only include non-empty sections
            summary_text += f"➜ {label}:\n" + " ".join(sentences) + "\n\n"

    print(summary_text)

sample_text = '''
Appeal No. 285 of 1959.
Appeal by Special Leave from the Judgment and Decree dated the 13th July, 1956, of the Patna High Court in M. J. C. No. 404 of 1954.
M. C. Setalvad, Attorney General for India and section P. Varma, for the Appellants.
A. V. Viswanatha Sastri, Suresh Aggarwala and D. P. Singh, for the Respondent. 1960.
November 21.
The Judgment of the Court was delivered by 524 SINHA, C.J.
This appeal, by special leave, is directed against the judgment and order of the High Court of Patna dated July 13, 1956 disposing of a reference under section 25(1) of the Bihar Sales Tax Act, 1947, which hereinafter will be referred to as the Act, made by the Board of Revenue, Bihar.
The facts of this case have never been in dispute and may shortly be stated as follows.
The appellant is a Corporation incorporated under the Damodar Valley Corporation Act (XIV of 1948) and will hereinafter be referred to as the Corporation.
It is a multipurpose Corporation, one of its objects being the construction of a number of dams in Bihar and Bengal with a view to controlling floods and utilising the stored water for purposes of generation of electricity.
One of such dams is the Konar Dam in the district of Hazaribagh in Bihar.
For the construction of the aforesaid Dam the Corporation entered into an agreement with Messrs Hind Construction Ltd. and Messrs Patel Engineering Co. Ltd. on May 24, 1950, and appointed them contractors for the aforesaid purpose.
They will hereinafter be referred to as the Contractors.
As a result of a change in the design of the Dam, it became necessary to enter into a supplementary agreement and on March 10, 1951, cl. 8 of Part II of the original agreement was amended and a fresh cl. 8 was substituted.
Under the new cl. 8 of the agreement, as amended, the Corporation agreed to make available to the contractors such equipment as was necessary and suitable for the construction aforesaid.
The Contractors are charged the actual price paid by the Corporation for the equipment and machinery thus made available, inclusive of freight and customs duty, if any, as also the cost of transport, but excluding sales tax.
The equipment thus supplied by the Corporation to the Contractors was classified into two groups, Group A and Group B, as detailed in Schedule No. 2.
The machinery in Group A was to be taken over from the Contractors by the Corporation, after the completion of the work at their "residual value" which was to be calculated in the manner set out in the agreement.
The machinery in Group B was to become the 525 property of the Contractors after its full price had been paid by them.
No more need be said about the machinery in Group B, because there is no dispute about that group, the Contractors having accepted the position that Group B machinery had been sold to them.
The controversy now remaining between the parties relates to the machinery in Group A.
On August 12, 1952, the Superintendent of Sales Tax, Hazaribagh, assessed the Corporation under section 13(5) of the Act for the period April, 1950 to March, 1952.
It is not necessary to set out the details of the tax demand, because the amount is not in controversy.
What was contended before the authorities below and in this Court was that the transaction in question did not amount to a "sale" within the meaning of the Act.
The Superintendent rejected the contention raised on behalf of the Corporation that it was not liable to pay the tax in respect of the machinery sup plied to the Contractors.
The Corporation went up in appeal to the Deputy Commissioner of Sales Tax against the said order of assessment.
By his order dated May 5, 1953, the Deputy Commissioner rejected the contention of the appellant as to its liability under the Act, but made certain amendments in the assessment which are not material to the points in controversy before us.
The Deputy Commissioner repelling the Corporation 's contentions based on the Act, held inter alia that the supply of equipment in Group A of the agreement aforesaid amounted to a sale and was not a hire ; that the condition in the agreement for the "taking over" of the equipment on conditions laid down in the agreement was in its essence a condition of repurchase and that the Corporation was a "dealer" within the meaning of the Act.
The Corporation moved the Board of Revenue, Bihar, in its revisional jurisdiction under section 24 of the Act.
The Board of Revenue by its resolution dated October 1, 1953, rejected the revisional application and upheld the order of the authorities below.
Thereafter, the Corporation made an application to the Board of Revenue under section 25 of the Act for a reference to refer the following 67 526 questions to the High Court at Patna, namely, (a) whether the assessment under section 13(5) of the Act is maintainable, (b) whether, in the facts and circumstances of the case, it can be held that the property in the goods included in Schedule A did pass to the Contractors and the transaction amounted to a sale, and (c) whether the terms of the agreement amount to sale transactions with the Contractors and taking over by the Corporation amounts to repurchase.
This application was made on December 22, 1953, but when the application for making a reference to the High Court came up for hearing before the Board of Revenue on May 20, 1954, and after the parties had been heard, counsel for the Corporation sought leave of the Board to withdraw questions (a) and (c) from the proposed reference and the Board passed the following order: "Leave is sought by the learned advocate for the petitioner to drop questions (a) and (c) from the reference.
The leave is granted.
There remains only question (b) for reference to the High Court. . " Thus only question (b) set out above was referred to the High Court for its decision.
After hearing the parties, a Division Bench of the High Court, Ramaswami, C. J. and Raj Kishore Prasad, J., heard the reference and come to the conclusion by its judgment dated July 13, 1956, that the reference should be answered in the affirmative, namely, that the transaction in question amounted to a sale within the meaning of section 2(g) of the Act.
Thereupon the Corporation made an application headed as under article 132(1) of the Constitution and prayed that the High Court "be pleased to grant leave to appeal to the Supreme Court of India and grant the necessary certificate that this case is otherwise a fit case for appeal to the Supreme Court. . " Apart from raising the ground of attack dealt with by the High Court on the reference as aforesaid, the Corporation at the time of the hearing of the applica tion appears to have raised other questions as would appear from the following extract from the judgment and order of the High Court dated January 31, 1957 : 527 "It was conceded by learned counsel for the petitioner that the case does not fulfill the requirements of Article 133(1) of the Constitution; but the argument is that leave may be granted under Article 132 of the Constitution as there is a substantial question of law with regard to the interpretation of the Constitution involved in this case.
We are unable to accept this argument as correct.
It is not possible for us to hold that there is any substantial question of law as to the interpretation of the Constitution involved in this case.
The question at issue was purely a matter of construction of section 2(g) of the Bihar Sales Tax Act and that question was decided by this Court in favour of the State of Bihar and against the petitioner.
It is argued now on behalf of the petitioner that the provisions of section 2(g) of the Bihar Sales Tax Act are ultra vires of the Constitution, but no such question was dealt with or decided by the High Court in the reference.
We do not, therefore, consider that this case satisfies the requirements of article 132(1) of the Constitution and the petitioner is not entitled to grant of a certificate for leave to appeal to the Supreme Court under this Article.
The application is accordingly dismissed.
" Having failed to obtain the necessary certificate from the High Court, the Corporation moved this Court and obtained special leave to appeal under article 136 of the Constitution.
The leave was granted on March 31, 1958.
Though the scope of the decision of the High Court under section 25 of the Act on a reference made to it is limited, the Corporation has raised certain additional points of controversy, which did not form part of the decision of the High Court.
Apart from the question whether the transaction in question amounted to a sale within the meaning of the Act, the statement of the case on behalf of the appellant raises the following additional grounds of attack, namely, (1) that the Corporation is not a dealer within the meaning of the Act, (2) that the proviso to section 2(g) of the Act is ultra vires the Bihar Legislature and (3) that the Act itself is ultra vires the Bihar Legislature by reason of the 528 legislation being beyond the scope of entry 48 in List II of Schedule 7 of the Government of India Act, 1935.
Hence, a preliminary objection was raised on behalf of the respondent that the additional grounds of attack were not open to the Corporation in this Court.
It is, therefore, necessary first to determine whether the additional grounds of attack set out above are open to the Corporation.
In our opinion, those additional grounds are not open.
They were never raised at any stage of the proceedings before the authorities below, or in the High Court.
This Court is sitting in appeal over the decision of the High Court under section 25 of the Act.
The High Court in coming to its conclusion was acting only in an advisory capacity.
It is well settled that the High Court acting in its advisory capacity under the taxing statute cannot go beyond the questions referred to it, or on a reference called by it.
The scope of the appeal to this Court, even by special leave, cannot be extended beyond the scope of the controversy that could have been legally raised before the High Court.
It is manifest that the High Court could not have expressed its opinion on any matter other than the question actually before it as a result of the reference made by the Board of Revenue.
The preliminary objection must, therefore, be allowed and the appeal limited to the question whether the transaction in question in this case amounted to a sale within the meaning of the Act.
It is manifest that this controversy between the parties has to be resolved with reference to the terms of the contract itself.
Clause 8 of the agreement as amended is a very complex one as will presently appear from the following extracts, being the relevant portions of that clause : "The Corporation may hire or make available such of its equipment as is suitable for construction for the use of the Contractor.
The actual prices paid by the Corporation for the equipment thus made available, inclusive of freight, insurance and custom duties, if any, and the cost of its transport to site but excluding such tax as sales tax whether local, municipal, State or Central, shall be charged to the 529 Contractor and the equipment shall remain the property of the Corporation until the full prices thereof have been realised from the Contractor.
Equipment lent for the Contractor 's use, if any, shall be charged to him on terms of hiring to be mutually agreed upon; such terms will cover interest on capital cost and the depreciation of the equipment.
The Corporation will supply to the Contractor the machinery mentioned in Schedule No. 2, Group A and Group B below." Then follows a description seriatim of the many items of machinery in Group A with the number of such machinery and the approximate cost thereof.
In this Group A, there are fourteen items of which it is only necessary to mention the first one, that is to say, four excavators with accessories approximately valued at Rs. 12,46,390; and No. 14, two excavators of another model, approximately costing Rs. 3,35,000.
The total approximate cost of the machinery in Group A is estimated to be Rs. 42,63,305.
Then follow the descriptions of machinery in Group B, the approximate cost of which is Rs. 21,84,148.
Then follow certain conditions in respect of equipments included in Group A, in these words: "The Corporation will take over from the Contractor item 1 and 14 on the completion of the work at a residual value calculated on the basis of the actual number of hours worked assuming the total life to be 30,000 hours and assuming that the machinery will be properly looked after during the period of its operation.
The remaining items of this group will be taken over by the Corporation at their residual value taking into account the actual number of hours worked and the standard life of such machinery for which Schedule F. as last relished, ? of the U. section Bureau of Industrial Revenue, on the probable useful life and depreciation rates allowable for Income Tax purpose (vide Engineering News Record dated March 17, 1949) will serve as a basis, provided that the machinery shall be properly looked after by the Contractor during the period of its operation.
Provided further that such residual value of the machinery shall be assessed 530 jointly by representatives of the Corporation and of the Contractor and that in case of difference of opinion between the two parties the matter shall be settled through arbitration by a third party to be agreed to both by the Corporation and the Contractor.
The items included in this group will be taken over by the Corporation from the Contractor either on the completion of the work or at an earlier date if the Contractor so wishes, provided that in the latter case the equipments will be taken over by the Corporation only when they are declared surplus at Konar and such declaration is duly certified by the Consulting Engineer, within a period of 15 days of such declaration being received by the Corporation.
In respect of the machinery which shall have been delivered to the Contractor on or before the 31st of December 1950, their cost shall be recovered from the Contractor in eighteen equal instalments beginning with January 1951 and in respect of the remaining items included in this group of machinery, their cost will be recovered from the Contractor in eighteen equal instalments beginning with July 1951, provided that these remaining items shall have been delivered to the Contractor prior to the last specified date.
Provided (a) that the total actual price for these equipments which has been provisionally estimated at Rs. 42,63,305 will be chargeable to the Contractor as per first para of clause 1 above.
(b) that after approximately two thirds of total cost or an amount of Rs. 28,43,000 (Rupees twenty eight lakhs forty three thousand) approximately has been recovered from the Contractor on account of these equipments the Corporation will consider the date or dates when it could take over the equipments still under use by the Contractor, assess the, extent to which they have already been depreciated and thereby arrive at, their residual value; and (c) that the recovery or refund of the amount payable by or to the Contractor on account of these equipments will be decided only if the Corporation is fully satisfied that their residual life at the time of 531 their being finally handed over to the Corporation shall under no circumstances fall below one third of their respective standard life as agreed upon by the Corporation and the Contractor." Then follow terms and conditions in respect of Group 'B ' which are not relevant to our purpose.
Thereafter, the following conditions appear: "In respect of equipments whether in Group A or B made available by the Corporation to the Contractor.
The following conditions shall apply to all equipments, i.e., those included in Group A and B above and others, if any (a) The Contractor shall continuously maintain proper machine cards separately in respect of each item of equipment, clearly showing therein, day by day, the number of actual hours the machine has worked together with the dates and other relevant particulars.
(b) The Contractor shall maintain all such equipments in good running condition and shall regularly and efficiently give service to all plant and machinery, as may be required by the Corporation 's Chief Engineer who shall have the right to inspect, either personally or through his authorised representatives all such plant and equipment and the machine cards maintained in respect thereof at mutually convenient hours.
(c) No item of equipment made available by the Corporation on loan or hire shall at any time be removed from the work site under any circumstances until the full cost thereof has been recovered from the Contractor by the Corporation and thereafter only if in the opinion of the Consulting Engineer the removal of such item or items is not likely to impede the satisfactory prosecution of the work.
Similarly no item of equipment or material belonging to the Contractor but towards the cost of which money has been advanced by the Corporation shall at any time be removed from the work site under any circumstances until the amount of money so advanced has been recovered from the Contractor by 532 the Corporation and thereafter if in the opinion of the Consulting Engineer the removal of such item or items is not likely to impede the satisfactory prosecution of the work.
(d) The Corporation shall supply to the Contractor whatever spares have been procured or ordered for the equipment already supplied or to be supplied by the Corporation to the Contractor under the terms of this Agreement and that thereafter the replenishment of the stock of spares shall be entirely the responsibility of the Contractor who shall therefore take active steps in time to procure fresh spares so as to maintain a sufficient reserve.
The spares to be supplied by the Corporation will be issued to the Contractor by the Executive Engineer, Konar as and when required by the Contractor against indent accompanied by a certificate that the spares previously issued to him have been actually used up on the machines for which they were intended.
(e) Whenever spares are issued to the Contractor in accordance with this provision, their actual prices inclusive of freight, insurance and customs but excluding storage and handling charges shall be debited against him and recovered from his next fortnightly bill.
(f) In order to enable the Contractor to take active steps for planning the procurement of additional spares in advance, the Corporation shall forthwith furnish to him a complete list of all the spares which it has procured or ordered for the equipment to be supplied to the Contractor.
" The portions quoted above contain the relevant terms and conditions in respect of the transaction in question, so far as it is necessary to know them for the purpose of this case.
It will be noticed that the Corporation made available to the Contractors different kinds of machinery and equipment detailed in Group A of the approximate value of Rs. 42,63,000 odd, for which the price paid by the Corporation inclusive of freight, insurance, customs duty etc.
has to be charged to them.
But the machinery and the equipment so 533 made available to the Contractors were to remain the property of the Corporation until the, full price thereof had been realised from the Contractors.
It is also noteworthy that the agreement makes a distinction between the aforesaid part of the agreement and the equipment lent to the contractors in respect of which the contractors had to be charged in terms of hiring, including interest on capital cost and the depreciation of equipment.
Thus clearly the agreement between the parties contemplated two kinds of dealings between them, namely (1) the supply of machinery and equipments by the Corporation to the Contractors and (2) loan on hire of other equipment on terms to be mutually agreed between them in respect of the machinery and equipment supplied by the Corporation to the Contractors.
There is a further condition that the Corporation will take over from the contractors items 1 and 14, specifically referred to above, and the other items in Group A at their "residual value" calculated on the basis indicated in the paragraph following the description of the machinery and the equipments.
But there is a condition added that the "taking over" is dependent upon the condition that the machinery will be properly looked after during the period of its operation.
There is an additional condition to the taking over by the Corporation, namely, the work for which they were meant had been completed, or earlier, at the choice of the Contractors, provided that they are declared surplus for the purposes of the construction of the Konar Dam and so certified by the Consulting Engineer.
Hence, it is not an unconditional agreement to take over the machinery and equipment as in Group B.
The total approximate price of Rs. 42,63,305 is payable by the Contractors in 18 equal instalments.
Out of the total cost thus made realisable from the Contractors two thirds, namely, Rs. 28,42,000 approximately, has to be realised in any case.
After the two thirds amount aforesaid has been realised from the contractors on account of supply of the equipments by the Corporation, the Corporation had to consider the date or dates of the "taking over" of the equipment after assessing the extent to which it 534 had depreciated as a result of the working on the project in order to arrive at the "residual value" of the same.
The refund of the one third of the price or such other sum as may be determined as the "residual value" would depend upon the further condition that the Corporation was fully satisfied that their "residual life" shall, under no circumstances, fall below one third of their respective standard life as agreed upon by the parties.
It would, thus, appear that the "taking over" of such of the equipments as were available to be returned was not an unconditional term.
The Corporation was bound to take them over only if it was satisfied that their "residual life" was not less than one third of the standard life fixed by the parties.
It is clear from the terms and conditions quoted above that there was no right in the contractors to return any of the machinery and equipments at any time they liked, or found it convenient to do so.
The conditions which apply to all equipments, whether in Group A or in Group B, are also relevant to determine the nature of the transaction.
The contractors are required to "continuously maintain proper machine cards showing certain relevant particulars".
It is their duty to maintain the equipments in good running condition and to regularly and effectively service them.
No item of machinery and equipment could be removed by the contractors under any circumstances until the full cost thereof had been recovered from them and even then only if the removal of those items of machinery or equipment was not likely to impede the satisfactory progress of the work.
Then follows the most important condition that the Contractors themselves shall have to replenish their stock of spare parts of the machinery made available to them by the Corporation.
When spare parts are supplied to the Contractors by the Corporation, they shall be liable for the actual price of those parts inclusive of freight, insurance and customs duty.
Those substantially are the terms of the contract between the parties and the sole question for determination in this appeal is whether, in respect of the machinery and equipments admittedly supplied by the Corporation to the Contractors, it was a mere 535 contract of hiring, as contended on behalf of the appellant Corporation, or a sale or a hire purchase, as contended on behalf of the respondent State.
The law on the subject is not in doubt, but the difficulty arises in applying that law to the facts and circumstances of a particular case on a proper construction of the document evidencing the transaction between the parties.
It is well settled that a mere contract of hiring, without more, is a species of the contract of bailment, which does not create a title in the bailee, but the law of hire purchase has undergone consider able development during the last half a century or more and has introduced a number of variations, thus leading to categories, and it becomes a question of some nicety as to which category a particular contract between the parties comes under.
Ordinarily, a contract of hire purchase confers no title on the hirer, but a mere option to purchase on fulfillment of certain conditions.
But a contract of hire purchase may also provide for the agreement to purchase the thing hired by deferred payments subject to the condition that title to the thing shall not pass until all the instalments have been paid.
There may be other variations of a contract of hire purchase depending upon the terms agreed between the parties.
When rights in third parties have been created by acts of parties or by operation of law, the question, which does not arise here, may arise as to what exactly were the rights and obligations of the parties to the original contract.
It is equally well settled that for the purpose of determining as to which category a particular contract comes under, the court will look at the substance of the agreement and not at the mere words describing the category.
One of the tests to determine the question whether a particular agreement is a contract of mere hiring or whether it is a contract of purchase on a system of deferred payments 'of the purchase price is whether there is any binding obligation on the hirer to purchase the goods.
Another useful test to determine such a controversy is whether there is a right reserved to the hirer to return the goods at any time during the subsistence of the contract.
If there is such a right reserved, then 536 clearly there is no contract of sale, vide Helby vs Matthews and others (1).
Applying these two tests to the transaction in the present case, it becomes clear that it was a case of sale of goods with a condition of repurchase on certain conditions depending upon the satisfaction of the Corporation as to whether the "residual life" of the machinery or the equipment was not less than one third of the standard life in accordance with the terms agreed between the parties.
It is clear on those terms that there is no right reserved to the contractors to return the goods at any time that they found it convenient or necessary.
On the other hand, they were bound to pay two thirds of the total approximate price fixed by the parties in equal instalments.
The Contractors were not bound under the terms to return any of the machinery or the equipments, nor was the Corporation bound to take them back unconditionally.
The term in the agreement regarding the "taking over" of the machinery or equipments by the Corporation on payment of the "residual value" is wholly inconsistent with a contract of mere hiring and is more consistent with the property in the goods having passed to the Contractors, subject to the payment of all the instalments of the purchase pride.
Furthermore, the stipulation that the Contractors themselves will have to supply the spare parts, as and when needed, for replacements of the worn out parts is also consistent with the case of the respondent that title had passed to the contractors and that they were responsible for the upkeep of the machinery and equipments and for depreciation.
If it were a mere contract of hiring, the owner of the goods would have continued to be liable for replacements of worn out parts and for depreciation.
Applying those tests to the terms of the agreement between the parties, it is clear that the transaction was a sale on deferred payments with an option to repurchase and not a mere contract of hiring, as contended on behalf of the appellant.
It must, therefore, be held that the judgment of the High Court is entirely correct and the appeal must be dismissed with costs.
Appeal dismissed.
'''

summarize_text(sample_text)
