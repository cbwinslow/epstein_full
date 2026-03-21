--
-- PostgreSQL database dump
--

\restrict yQ0uosZjIwsK7EKQ5uzLgBWLBSbLuzWaymyt36Ju2t3begYaZLvwggHPbQVq0vk

-- Dumped from database version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.13 (Ubuntu 16.13-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: communication_pairs; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.communication_pairs (id, person_a, person_b, email_count, first_date, last_date, a_to_b_count, b_to_a_count, sample_subjects, sample_eftas) FROM stdin;
560	Alexander Acosta	Jeff Sloman	1	\N	\N	0	1	["Epstein Rolando informs me that Krischer said that the plea & sentencing will take place on the same day (December 16th ) in order to reduce the media frenzy. Krischer said that Epstein will be treate"]	["EFTA00189193"]
561	Alexander Acosta	Jay Lefkowitz	2	\N	\N	0	2	["Re: Epstein Dear Jeff: I received your email yesterday and was a little surprised at the tone of your letter, given the fact that we spoke last week and had what I thought was a productive meeting. I ", "Follow up Alex - I wanted to thank you for making the time for"]	["EFTA00189202", "EFTA00214928"]
562	Jay Lefkowitz	Jeff Sloman	1	\N	\N	1	0	["Re: Epstein Dear Jeff: I received your email yesterday and was a little surprised at the tone of your letter, given the fact that we spoke last week and had what I thought was a productive meeting. I "]	["EFTA00189202"]
563	Bradley Edwards	Paul Cassell	26	\N	\N	1	25	["RE: 0PR inquiry - request for information - 4 PM today? Great \\u2014 what number should we call? Paul EFTA00205028", "RE: OPR complaint Hi Thanks for getting back to me. I was confused about one point \\u2014 my letter to U.S. Attorney Ferrer requesting further investigation of the Epstein matter didn't appear to me to rai", "RE: Discovery Issues in Epstein", "RE: One additional discovery request in Jane Doe #1 and Jane Doe #2 vs. U.S., No. 08-80736 Dear I am writing to confirm that you remain the person that we should be contacted with regard to the above-", "RE: One additional discovery request in Jane Doe #1 and Jane Doe #2 vs. U.S., No. 08-80736 Dear I am writing to confirm that you remain the person that we should be contacted with regard to the above-"]	["EFTA00210971", "EFTA00206871", "EFTA00205035", "EFTA00210525", "EFTA00205269", "EFTA00210838", "EFTA00205274", "EFTA00206659", "EFTA00206692", "EFTA00209732"]
564	Jay Lefkowitz	Roy Black	1	\N	\N	1	0	["Re: Jane Does United States"]	["EFTA00227071"]
565	Jeffrey Epstein	Richard Kahn	437	2011-11-10	2019-05-22	350	87	["Fwd: Support Caitlin's Team, Young NYC, in the Crohn's and Colitis Foundation Take Steps Walk", "Re:", "take a confidential look, . mid cabin seats to be removed cabinets built. seats need to recline however , railing will have to be modifited to elimante third seat drink side tables etc.. sofa made lik", "take a confidential look, . mid cabin seats to be removed cabinets built. seats need to recline however , railing will have to be modifited to elimante third seat drink side tables etc.. sofa made lik", "Fwd: Reminder Music for car in Paris have james download all my laptop music onto four thumbdrives. thanks"]	["EFTA00370047", "EFTA00313080", "EFTA00370035", "EFTA00370044", "EFTA00366977", "EFTA00328610", "EFTA00357744", "EFTA00328608", "EFTA00344450", "EFTA00327453"]
566	Darren Indyke	Richard Kahn	57	2014-03-24	2018-01-29	20	37	["Fwd: Fwd: RE:", "Re: Chairs at the Gotham Awards", "Re: FWB invoices Lilly, >; CHRISTOPHER E. KNIGHT", "Re: Citi Preferred [C] please work $3,000,000 order at 100.00 for Citi Preferred Q please email or call Darren if you need to confirm thank you Richard Kahn", "Fwd: Link a Rockenbach Revised June Bill"]	["EFTA01047433", "EFTA01401792", "EFTA00799164", "EFTA00901772", "EFTA01352611", "EFTA00851394", "EFTA01000615", "EFTA01040974", "EFTA01401427", "EFTA00849350"]
567	Karyna Shuliak	Lesley Groff	13	2016-03-15	2018-10-03	6	7	["Re: Picture you requested 2 of 2 Thank you for all of your help! We can certainly wait for you to speak with them on Tuesday \\u2014appreciate it Lesley On Sep 25. 2016. at 3:59 AM. TYOGH-Shared MB-Concierg", "Reservations for visa", "Reservations for visa", "Jeffrey Epstein Hello Ion. Hope you are well. Jeffrey is wondering if you are in NY or plan to come to NY soon. He has a project at the apartments he is hoping you could tackle for him. Please let me ", "WiFI Issues"]	["EFTA02043374", "EFTA02142428", "EFTA00449225", "EFTA02043467", "EFTA02059849", "EFTA00327925", "EFTA02329710", "EFTA00327919", "EFTA00337206", "EFTA00714261"]
568	Andrew Farkas	Lesley Groff	10	\N	\N	0	10	["Re: Jeffrey Epstein I just noticed you have", "Re: le ey pstein Passenger List: Jeffrey Epstein On Jul 25, 2016, at 11:57 AM, Dowling, David > wrote: Richard, See below and attached. you are all set for Wednesday. I have also included heliflite on", "Jeffrey Epstein >; Hello Andrew. I understand you will be visiting Jeffrey on his island late morning of Jan. 2nd. I have cc'd on this mail who take care of Jeffrey's island. Their cell phone numbers ", "Jeffrey Epstein Hello Andrew. I understand you will come see Jeffrey for breakfast at 8:30 Monday morning. Would you", "Jeffrey Epstein Hello Andrew. I understand you will come see Jeffrey for breakfast at 8:30 Monday morning. Would you"]	["EFTA00950869", "EFTA00321442", "EFTA00398774", "EFTA00420791", "EFTA02175460", "EFTA00420789", "EFTA00420787", "EFTA02175531", "EFTA00321647", "EFTA02175583"]
569	Lesley Groff	Richard Kahn	64	2014-11-06	2017-05-04	32	32	["Re: Jeffrey Epstein I just noticed you have", "Re: Jeffrey Epstein Can you please change departure to 5:30pm from bard college to 34th street. In addition j have not yet seen", "Re: >", "Re: >", "Re: le ey pstein Passenger List: Jeffrey Epstein On Jul 25, 2016, at 11:57 AM, Dowling, David > wrote: Richard, See below and attached. you are all set for Wednesday. I have also included heliflite on"]	["EFTA00446423", "EFTA00321759", "EFTA00336301", "EFTA00337206", "EFTA00362581", "EFTA00321647", "EFTA00380147", "EFTA00321613", "EFTA00367534", "EFTA00446428"]
570	Larry Visoski	Richard Kahn	40	2015-10-23	2017-11-09	15	25	["Re: Jeffrey Epstein Can you please change departure to 5:30pm from bard college to 34th street. In addition j have not yet seen", "Re: Jeffrey Epstein thank you for email my understanding is that they will be landing on bard campus which is what was done in the past On Jul 25, 2016, at 11:57 AM, Dowling, David < > wrote: Richard,", "Re: Jeffrey Epstein thank you for email my understanding is that they will be landing on bard campus which is what was done in the past On Jul 25, 2016, at 11:57 AM, Dowling, David < wrote: Richard, S", "Re: Jeffrey Epstein thank you for email my understanding is that they will be landing on bard campus which is what was done in the past On Jul 25, 2016, at 11:57 AM, Dowling, David <I", "Fwd: [External] Epstein charter confirmed mailto: To all, Ref: Epstein S76 charter July 26, 2014 10:00am local departure from West Side NYC heli pad.,to South Hampton Beach heli pad., Gregory, AAG"]	["EFTA00368121", "EFTA00321759", "EFTA00374778", "EFTA00932571", "EFTA00409641", "EFTA00632089", "EFTA00369226", "EFTA00375060", "EFTA01028741", "EFTA00863936"]
571	Bella Klein	Lesley Groff	29	2016-02-05	2019-05-16	6	23	["Nili re a 2nd router", "Nili re a 2nd router", "Re: Jeffrey Epstein great! thanks bella On Apr 22, 2015, at 3:13 PM, bellaklein < > wrote: EFTA00348664", "Jeffrey Epstein Hello Allison...I have asked Bella in our accounting department to please have a look to see if phone number", "Re: FW:"]	["EFTA02045032", "EFTA02059914", "EFTA02196616", "EFTA02098235", "EFTA02098257", "EFTA00362581", "EFTA02177453", "EFTA00348663", "EFTA01992090", "EFTA00321516"]
735	Marvin Minsky	Richard Kahn	2	\N	\N	2	0	["Re: Mr. Epstein Oh, good. I'm sure NN will like it too, because he suggested it. Also, Cynthia Solomon has been a consultant to", "Re: Mr. Epstein Oh, good. I'm sure NN will like it too, because he suggested it. Also, Cynthia Solomon has been"]	["EFTA00758534", "EFTA02423930"]
572	Jeffrey Epstein	Lesley Groff	208	2014-08-13	2019-04-22	149	59	["Nili re a 2nd router", "Nili re a 2nd router", "Re: Dinner tonight-who to organize EFTA00322669", "Re: french, send to her geneve house On Tue, Feb 23, 2016 at 11:04 PM, <nmyhrvold@gmail.com> wrote:", "Re: Rich and Darren > wrote: does today work? On Wed, Feb 17, 2016 at 1:03 PM, Lesley Groff <I > wrote:"]	["EFTA00336431", "EFTA00364677", "EFTA00333380", "EFTA00358716", "EFTA00333377", "EFTA00352564", "EFTA00321516", "EFTA00355735", "EFTA00328196", "EFTA00328862"]
573	Lesley Groff	Peter Attia	21	\N	\N	20	1	["Jeffrey's MRI Report EFTA00321893", "Re: update No worries there! We will send our maid In to take care of all. Hope you get the apt soon! What a headache! Please let me know around what time you plan to vacate the apt. Thx, lesley Sent ", "Re: update No worries there! We will send our maid In to take care of all. Hope you get the apt soon! What a headache! Please let me know around what time you plan to vacate the apt. Thx, lesley Sent ", "Re: Jeffrey Epstein Mary lets discuss before you change things! Jeffrey is flexible! (thanks Peter!) On Jul 9, 2017, at 5:44 PM, Peter Attia < > wrote:", "Re: Meeting with JE"]	["EFTA00459844", "EFTA00460664", "EFTA00330627", "EFTA00460661", "EFTA00321892", "EFTA00630979", "EFTA02062015", "EFTA02062385", "EFTA00679177", "EFTA02471926"]
574	Jeffrey Epstein	Peter Attia	126	\N	\N	123	3	["Re: Fwd: 7am On Sun, Jul 17, 2016 at 6:52 PM, Peter Attia 4 wrote:", "Re: I leave new york the 7th, are you ok with the resolution?! On Wed, Dec 30, 2015 at 9:53 AM, Peter Attia c wrote: Thanks for checking in Jeffrey. It's been a hell of a stretch. Resolution reached o", "Re: Re: night of 6th good On Wed, Dec 30, 2015 at 10:00 AM, Peter Attia < > wrote: I. What time do you leave? I actually get in on the 6th and can try to rearrange schedule if you have time the night ", "Re: pswd demosterol looks wild On Tue, Feb 16, 2016 at 9:59 PM, Peter Attia myhdl wrote: Peter Attia, M.D. Attia Medical, PC (m) The information contained in this transmission may contain privi eged a", "figure it out yet please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of"]	["EFTA00643671", "EFTA00851428", "EFTA00842987", "EFTA00851442", "EFTA00851433", "EFTA00823782", "EFTA00322218", "EFTA00332735", "EFTA00813487", "EFTA00689728"]
575	David Mitchell	Jeffrey Epstein	67	2011-05-09	2018-10-22	10	57	["Re: ok On Tue, Jun 21, 2016 at 5:28 AM, David Mitchell < Great ,Can we do the afternoon, I will ask Lesley DAVID MITCHELL Mitchell Holdings LLC 801 Madison Avenue New York NY 10065 USA 1212-486-4444 O", "Re: ok On Tue, Jun 21, 2016 at 5:28 AM, David Mitchell < Great ,Can we do the afternoon, I will ask Lesley DAVID MITCHELL Mitchell Holdings LLC 801 Madison Avenue New York NY 10065 USA On Jun 21, 2016", "Re: this week is good On Mon, Feb 13, 2012 at 6:53 AM, David Mitchell <I Hope you are great, Are you back in NY ,if not I hope in someplace warm, If you are can I see you this week, David, Sent via Bl", "Re: I find restaurants confining, .. would you be open to having dinner at my house., conversations are more lively", "Re: thnaks On Mon, May 9, 2011 at 3:58 PM, David Mitchell < at 5pm today DAVID MITCHELL Mitchell Holdings LLC 815 FIFTH AVENUE New York NY 10065 USA"]	["EFTA00675040", "EFTA00898225", "EFTA00777899", "EFTA00753295", "EFTA00753298", "EFTA00631866", "EFTA00917046", "EFTA00323560", "EFTA00823109", "EFTA00323525"]
576	Lesley Groff	Nicholas Ribis	4	\N	\N	4	0	["Re: Jeffrey epstein Exactly! I hope to hear from him today but it may be tomorrow morning before I get an answer! Will get back to you as soon as I can! Sent from my iPhone On May 17, 2016, at 10:33 A", "Re: Jeffrey epstein Hi Nick. Could you come see Jeffrey today at noon?", "Jeffrey Epstein > wrote: Hello Nick. Jeffreys home address is 9East 71st street between 5th and Madison. Will the l lam tomorrow work for you? Lesley Assistant to Jeffrey Epstein Sent from my iPhone E", "Jeffrey Epstein Hello Nick. Jeffreys home address is 9East 71st street between 5th and Madison. Will the 11 am tomorrow work for you? Lesley Assistant to Jeffrey Epstein Sent from my iPhone EFTA003331"]	["EFTA00324718", "EFTA00324721", "EFTA00333143", "EFTA00333126"]
577	Jeffrey Epstein	Noam Chomsky	194	\N	\N	190	4	["Re: 1 EFTA00325126", "Re: Re:", "Re:", "Re:", "Re: I understand, mathematics are the unique formalism for proofs. . I watch the lack of direction and leadership. , as in cognitive theory, with lots of data and no much beter understanding, I m tryi"]	["EFTA00329206", "EFTA00626491", "EFTA00644413", "EFTA00645754", "EFTA00329213", "EFTA00637798", "EFTA00658355", "EFTA00645713", "EFTA00666786", "EFTA00325125"]
578	Lesley Groff	Paul Morris	30	2013-04-23	2014-06-04	30	0	["Re: Checking in sure...let me get back to you! On Apr 25, 2016, at 11:29 AM, Paul Morris < Classification: Public Thanks Lesley, can you get me on his calendar for Wednesday? Paul Morris Managing Dire", "Re: (CI Hi Paul. Morning! Were you hoping to see Jeffrey or just speak with him? Sent from my iPhone On Mar 1, 2016, at 4:25 PM, Paul Morris wrote: Classification: Confidential Hi is je around tomorro", "Re: Jeffrey Epstein", "Re: Hello I HI Paul...Jeffrey is asking to speak with you...could you please give a call: Thanks, Lesley OnApr23,2013,at10:25AM,PaulMorriswrote: Classification: Public Hi Lesley, hope you're well. Is ", "Jeffrey Epstein Hello paul. Jeffrey will be in town next week and hens asking I you could cone see him on Tuesday at his home. I know you tend to like later in the day. would 5pm be good for you? Lesl"]	["EFTA01351316", "EFTA01351494", "EFTA00328665", "EFTA01351543", "EFTA00460508", "EFTA00460577", "EFTA01351538", "EFTA00373877", "EFTA00460572", "EFTA00410843"]
579	Jeffrey Epstein	Martin Weinberg	28	2009-04-24	2009-04-24	22	6	["Re:", "Re:", "Re:", "Re: ATTORNEY-CLIENT PRIVILEGE", "Re:"]	["EFTA00743005", "EFTA00732477", "EFTA00905860", "EFTA00697839", "EFTA00649315", "EFTA00906567", "EFTA00774250", "EFTA00718250", "EFTA00638104", "EFTA00702800"]
580	Joi Ito	Lesley Groff	5	\N	\N	5	0	["JE and TP", "Re: Trip to the Island - Nov 29-30?", "Re: Trip to the Island - Nov 29-30? EFTA00362237", "Re: Trip to the Island - Nov 29-30?", "Re: Trip to the Island - Nov 29-30?"]	["EFTA00327660", "EFTA00362236", "EFTA00362644", "EFTA00362223", "EFTA00362623"]
581	Jeffrey Epstein	Joi Ito	32	2016-11-30	2016-11-30	0	32	["JE and TP", "Re: Trip to the Island - Nov 29-30?", "Re: Trip to the Island - Nov 29-30? EFTA00362237", "Re: Trip to the Island - Nov 29-30?", "Re: Trip to the Island - Nov 29-30?"]	["EFTA00327686", "EFTA00377501", "EFTA00448197", "EFTA00439637", "EFTA00448189", "EFTA00448167", "EFTA00448201", "EFTA00362236", "EFTA00814229", "EFTA00377505"]
595	Darren Indyke	Jeffrey Epstein	68	2014-11-04	2018-12-05	18	50	["Re: Founding Member Note & Amended Membership Plan", "Re: Opinion from 11th Circuit attached Let's have a call first thing on Monday. Please let", "Privileged and Confidential", "Privileged and Confidential", "Fwd: EPSTEIN I Fencelli - Rendez-vous FANCELLI -EPSTEIN"]	["EFTA00732477", "EFTA00351836", "EFTA00393236", "EFTA00390037", "EFTA00422935", "EFTA00649595", "EFTA00370981", "EFTA00407018", "EFTA00656016", "EFTA00407014"]
785	Boris Nikolic	Tom Pritzker	2	\N	\N	0	2	["Boris,", "Boris, After lunch tomorrow or Saturday breakfast works for me. I will be at the TEDx"]	["EFTA02028450", "EFTA01773805"]
582	Jeffrey Epstein	Nathan Myhrvold	34	2013-08-02	2013-08-02	34	0	["Re: french, send to her geneve house On Tue, Feb 23, 2016 at 11:04 PM, <nmyhrvold@gmail.com> wrote:", "-- time to speak? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the address", "-- time to speak? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the address", "-- time to speak? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the address", "EFTA00392423"]	["EFTA01842439", "EFTA01738366", "EFTA00721133", "EFTA00751440", "EFTA00419322", "EFTA01770482", "EFTA00392415", "EFTA00392417", "EFTA01960782", "EFTA00392429"]
583	Jeffrey Epstein	Larry Visoski	50	2015-03-20	2017-05-02	35	15	["Re: Hell and we will pre clear tomorw. return thurs wheel up 6 On Tue, Jan 26, 2016 at 7:12 AM, Larry Visoski c wrote: Jeffrey What time do you want Heli now? 9am? Or still 10am? I'm going to fuel hel", "Re: Hell and we will pre clear tomorw. return thurs wheel up 6 On Tue, Jan 26, 2016 at 7:12 AM, Larry Visoski c wrote: Jeffrey What time do you want Heli now? 9am? Or still 10am? I'm going to fuel hel", "NY arrival", "Re: 6th floor screen NYC buy a new projector screen, no worry about tomr night On Tue, Sep 1, 2015 at 3:59 PM, Larry Visoski c wrote: Jeffrey", "Re: I might have you fly sat to phonic without me and back On Thursday, March 19, 2015, Larry Visoski c wrote: Perfect thx,.Dave arrives Friday 4pm., Saturday, 4pm -talk & Text Thx Larry Sent from my "]	["EFTA00330495", "EFTA00331680", "EFTA00972056", "EFTA00330498", "EFTA01957921", "EFTA01044470", "EFTA00972229", "EFTA00340774", "EFTA01943090", "EFTA00351015"]
584	Lesley Groff	Michelle	5	\N	\N	5	0	["Re: Regal Domestics, Inc. - resumes", "Re: interview schedule EFTA_R1_00613994 EFTA02064323", "Re: interview schedule Hi Michelle and thank you very much for this! All the appointments work well with Jeffrey's schedule and are confirmed...Please do send along the bits and pieces still needed on", "Re: interview schedule perfect! thank you! \\u2022", "Re: interview schedule"]	["EFTA02064328", "EFTA00332464", "EFTA02064702", "EFTA02064322", "EFTA02064472"]
585	Darren Indyke	Lesley Groff	15	2015-04-23	2018-05-22	7	8	["Re: Meet w/JE this week?", "Re: Joe Pagano-Confidentiality Agreement", "Re: ,Japanese Visa Don-please review ASAP", "Re: Founding Member Note & Amended Membership Plan", "Re: Case Great. Thx so much. Below are dial in details you can distribute ... Or let me know who to send to and I will. Darren, can you be the leader? Toll-free dial-in number (U.S. and Canada): Inter"]	["EFTA00437018", "EFTA00376224", "EFTA00351836", "EFTA00442953", "EFTA00376197", "EFTA00390649", "EFTA00394252", "EFTA00475065", "EFTA00437092", "EFTA00334004"]
586	Kathryn Ruemmler	Lesley Groff	1	\N	\N	1	0	["Re: Jeffr Hi Lesley, My home address in DC is: It is fine to ship things there, but the only issue is that if there is signature required, then no one is there to sign if I am not home. That said, I h"]	["EFTA00334590"]
587	Lesley Groff	Noam Chomsky	4	\N	\N	4	0	["Re: Jeffrey Epstein", "Jeffrey Epstein", "Jeffrey Epstein", "Jeffrey Epstein"]	["EFTA02246493", "EFTA00338495", "EFTA00474081", "EFTA00536569"]
588	Lawrence Krauss	Lesley Groff	2	2015-10-01	2015-10-01	2	0	["Re: Your Ritz Holiday", "Re: Call with Jeffrey Epstein 530 pm would be better. I land at 440 pm t. An I h ve to get bags and head to my place. Either way, cell phon is good. If it is after 645 pm or so I will be in my office "]	["EFTA00338657", "EFTA02423373"]
589	Jeffrey Epstein	Martin Nowak	3	\N	\N	3	0	["Re:", "; Joi Ito < > president QIU , has suggested you as point of contact . I proposed to find your best and brightest and invite"]	["EFTA00714150", "EFTA00339963", "EFTA01873966"]
590	Jeffrey Epstein	Reid Weingarten	31	\N	\N	31	0	["Re: did it say that 1, cheryl as standing with you when you called her? cheryl called and told Bauer? On Tue, Jun 16, 2015 at 6:57 AM, Weingarten, Reid < wrote: Cheryl sent her an awful email", "15 16 17 ny? \\u25a0********************************************************** The information contained in this communication is", "Re: Next week? On Friday, January 18, 2013, Jeffrey Epstein wrote: palm beach", "Re: RE: I thought you should see him explaining that Jesus will rule from Missouri . I will be back for one day on thurs . We should talk bill and future fun Sony for all the typos .Sent from my iPhon", "Re: RE: Re: What happened to trial . When do you get there, Miami"]	["EFTA00419247", "EFTA00467755", "EFTA00854114", "EFTA00870270", "EFTA00397513", "EFTA00870255", "EFTA00467776", "EFTA00859978", "EFTA00683460", "EFTA00668836"]
591	Richard Joslin	Richard Kahn	14	\N	\N	6	8	["Re: i am too busy today to meet Samantha however Jeffrey would like to Skype with her today at 1pm from your office please arrange thank you Richard Kahn", "RE: Availability", "Re: Availability Can you please have Samantha come to my office for interview 575 Lexington Avenue - 4th Floor Thank you Rich On 3/26/15, 10:21 AM, \\"Richard Joslin\\" < wrote: Tmo at 12:15 at our office", "RE: Availability", "AP SHL Investors We did receive a K-1 after the FTC 2012 tax return was filed. They historically have sent us our K-1 every year after or"]	["EFTA02082000", "EFTA00643261", "EFTA00861294", "EFTA01194373", "EFTA02507993", "EFTA00861298", "EFTA02351764", "EFTA02507955", "EFTA00350339", "EFTA00693690"]
592	Jeffrey Epstein	Richard Joslin	157	2014-05-09	2014-05-09	96	61	["Re: Brad does not today work for Skype On Friday, March 27, 2015, Richard Joslin < > wrote: Samantha is not able to be in NYC on Monday as she is in NJ office of Untracht Early. I will look to see", "Re: Ok i am available at your convenience On Sunday, November 24, 2013, Jeffrey Epstein wrote:", "Re: Ok i am available at your convenience On Sunday, November 24, 2013, Jeffrey Epstein wrote:", "RE: Availability", "RE: Availability"]	["EFTA00631050", "EFTA00364691", "EFTA00634778", "EFTA00683934", "EFTA00693241", "EFTA00364675", "EFTA00350353", "EFTA00637918", "EFTA00365051", "EFTA00643313"]
593	Jeffrey Epstein	Jes Staley	9	2010-08-24	2010-08-24	6	3	["Re: Where are you?", "RE: Re:", "RE: Re:", "I think we should prepare to short the israeli market.. lets find a good way to play the uncertainty in the area The information contained in this communication is confidential, may be attorney-client", "Fwd: Maria"]	["EFTA00743944", "EFTA00697062", "EFTA00351232", "EFTA00377860", "EFTA00651481", "EFTA00766580", "EFTA00743948", "EFTA01626167", "EFTA01946324"]
594	Cecile de Jongh	Jeffrey Epstein	76	2016-08-28	2016-08-28	22	54	["Re: april 2. 3pm office On Wed, Mar 18, 2015 at 1:59 PM, Cecile de Jongh Adriane has the following times available: > wrote: April 1st - anytime after 2:30PM April 2nd - 2PM or after April 3rd - 2PM o", "Fwd: Meeting Request EFTA00406336", "Re: Meeting Request", "Re: Meeting Request", "Re: Meetingfrequest"]	["EFTA00406335", "EFTA00406351", "EFTA00428911", "EFTA00659607", "EFTA00351567", "EFTA00881141", "EFTA00897256", "EFTA00649106", "EFTA00752308", "EFTA00752531"]
791	Antoine Verglas	Lesley Groff	1	\N	\N	1	0	["Fwd: LittleStJames_JPEG"]	["EFTA01949922"]
596	Daphne Wallace	Lesley Groff	10	2015-02-02	2016-06-08	6	4	["Re: I Greetings Carlos,", "Jeffrey Epstein Hello Carlos. Jeffrey would like to order the same Inspire Fitness machine he has in PB for his island (reminder: this is the second one we ordered with the leg extension) Can you plea", "Jeffrey Epstein Hello Carlos. Jeffrey would like to order the same Inspire Fitness machine he has in PB for his island (reminder: this is the second one we ordered with the leg extension) Can you plea", "Re: Fw: Call Greetings David,", "Re: Fw: Call Greetings David,"]	["EFTA00496408", "EFTA00457880", "EFTA00353492", "EFTA02084178", "EFTA02151356", "EFTA02289937", "EFTA00353496", "EFTA02049467", "EFTA00457249", "EFTA00352101"]
597	Daphne Wallace	Richard Kahn	64	2016-06-02	2018-09-20	36	28	["Re: I Greetings Carlos,", "Re: AYH/Big N: Fenders bobby never responded to your last email nor contacted me can you please provide update on barge repairs along with expected return date to STT thanks Richard Kahn", "Fwd: duc duc beds - product info + pricing it was nice talking with you earlier", "Re: duc duc beds - product info + pricing S-\\u2022 thank you for working with us on price please adjust invoice for 11,575 and we will make deposit tomorrow", "Re: duc duc beds - product info + pricing thank you for working with us on price please adjust invoice for 11,575 and we will make deposit tomorrow"]	["EFTA00540626", "EFTA00540592", "EFTA00826329", "EFTA00547908", "EFTA00546553", "EFTA00546547", "EFTA00541460", "EFTA00547656", "EFTA00495985", "EFTA00548168"]
598	Cecile de Jongh	Darren Indyke	2	2015-02-03	2015-02-03	2	0	["Fw: TFL Application", "Roof Leak Darren, I would like to suggest that we at FTC, Inc. put our rental payments in escrow until the landlord fixes the roof. I have sat in this office for the past 11 years and had to endure ro"]	["EFTA00353302", "EFTA00733360"]
599	Lesley Groff	Richard Joslin	2	\N	\N	2	0	["Re: JEE HI Rich...do you need Jeffrey to have the package tomorrow? or Monday?", "Re: Tax returns Excellent. Thanks Sent from my iPhone rnailto Karyna Shuliak On Sep 8, 2015, at 7:09 PM, John Castrucci"]	["EFTA02072932", "EFTA00353364"]
600	Lesley Groff	Wallace Cunningham	2	\N	\N	2	0	["Jeffrey Epstein Hello Wally. Jeffrey would like to leave his island Saturday morning and fly to Palm Beach, FL. He could fly you in his plane with him to PB and then you could make the below connectio", "Jeffrey Epstein"]	["EFTA00353713", "EFTA02086385"]
601	Bella Klein	Richard Kahn	156	2014-05-16	2019-02-14	98	58	["Re: FPU", "Re: FPU", "Wire transfer instructions", "Re: amex", "Amex fraud Dateutgi\\u2022ust 10, 2012 10:51:07 AM EDT"]	["EFTA00359783", "EFTA00547581", "EFTA00547780", "EFTA00533519", "EFTA00540362", "EFTA00439257", "EFTA00547578", "EFTA00550851", "EFTA00354228", "EFTA00549892"]
602	Daphne Wallace	Jeffrey Epstein	17	2016-01-04	2016-01-04	6	11	["do we have my local boaters option number somewhere on file please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside inform", "do we have my local boaters option number somewhere on file please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside inform", "lets submit the minor permits today. jp we moved some of the huts , to other than xmas cove areas as per your suggeston please note The information contained in this communication is confidential, may", "Re: GSJ Minor Permit-Parcel Remainder A flagpole is in wrong location, it is on holy shit point", "Photos - September 1, 2015"]	["EFTA00639725", "EFTA01873781", "EFTA02694880", "EFTA01880849", "EFTA00677709", "EFTA02011056", "EFTA00355735", "EFTA02338705", "EFTA00355729", "EFTA01938441"]
603	Jeffrey Epstein	Reid Hoffman	59	\N	\N	59	0	["spoke to bill, hes glad you are coming, jet will pick you up in bedford anytime conveneint thurs eve, return you by noon friday please note The information contained in this communication is confident", "spoke to bill, hes glad you are coming, jet will pick you up in bedford anytime conveneint thurs eve, return you by noon friday please note The information contained in this communication is confident", "spoke to bill, hes glad you are coming, jet will pick you up in bedford anytime conveneint thurs eve, return you by noon friday please note The information contained in this communication is confident", "Re: yes, to logan ok for 930 pick up On Mon, Dec 1, 2014 at 10:11 PM, Reid Hoffman <I > wrote: I have a thurs dinner... when does the airport close? is it possible to do Logan instead? ideal would be ", "spoke to bill, hes glad you are coming, jet will pick you up in bedford anytime conveneint thurs eve, return you by noon friday please note The information contained in this communication is confident"]	["EFTA00357380", "EFTA00357388", "EFTA00528609", "EFTA00981861", "EFTA00357773", "EFTA00372249", "EFTA00357769", "EFTA00372256", "EFTA00357385", "EFTA00357771"]
604	Lesley Groff	Peggy Siegal	18	\N	\N	14	4	["Jeffrey Epstein Good Morning Peggy...Jeffity is coming to NY...he will be here Wed, Thur, Fri and perhaps Sat...He is asking if you might have anything going on? Please let us know! Thank you, Lesley ", "Jeffrey Epstein Good Morning Peggy...Jeffity is coming to NY...he will be here Wed, Thur, Fri and perhaps Sat...He is asking if you might have anything going on? Please let us know! Thank you, Lesley ", "Re: Conference Call terrific! I will pass along to Jeffrey...and just FYI, I'm pretty sure the check has been written and was sent already! On Nov 15, 2013, at 1:35 PM, Peggy Siegal wrote: This is rid", "Re: Conference Call ; Lyndsi Turner; terrific! I will pass along to Jeffrey...and just FYI, I'm pretty sure the check has been written and was sent already! On Nov 15, 2013, at 1:35 PM, Peggy Siegal w", "Jeffrey Epstein Good morning Peggy. Jeffrey is available for you to come see him today at the house at 2pm! Does this time still work for you? Lesley Sent from my iPhone EFTA00385297"]	["EFTA02395975", "EFTA00385320", "EFTA01969210", "EFTA02242309", "EFTA00379738", "EFTA00694050", "EFTA00471847", "EFTA00434936", "EFTA01760192", "EFTA00358716"]
605	Janusz Banasiak	Lesley Groff	2	\N	\N	0	2	["Re: Please take picture of Gym for Jeffrey Great.! thank you! hoping this will be helpful for you Carlos! On Nov 6, 2014, at 10:11 AM, Janusz Banasiak < > wrote: ok here they are<DSC_1673.jpeg><DSC_16", "Re: Please take picture of Gym for Jeffrey Great.! thank you! hoping this will be helpful for you Carlos! On Nov 6, 2014, at 10:11 AM, Janusz Banasiak < > wrote: ok here they are<DSC_1673.jpeg><DSC_16"]	["EFTA00359465", "EFTA00359467"]
606	Joi Ito	Reid Hoffman	11	\N	\N	11	0	["Re: Trip to the Island - Nov 29-30?", "Re: Trip to the Island - Nov 29-30? EFTA00362237", "Re: Trip to the Island - Nov 29-30?", "Re: Trip to the Island - Nov 29-30?", "Re:"]	["EFTA02118673", "EFTA00362236", "EFTA00377505", "EFTA00362223", "EFTA00362644", "EFTA00377501", "EFTA00362623", "EFTA02118609", "EFTA02118510", "EFTA00869398"]
642	Emad Hanna	Lesley Groff	3	\N	\N	0	3	["please send me your new email", "Re: tomorrow EFTA_R1_00888205 EFTA02190352", "Re: tomorrow totally makes sense to me On Mar 31, 2011, at 2:08 PM, Emad Hanna wrote: Will do I would guess should be cancelled so I don't want to waist the day Thank you Emad Hanna Project Controller"]	["EFTA00437131", "EFTA02190351", "EFTA02190381"]
643	Harry Beller	Lesley Groff	1	\N	\N	0	1	["please send me your new email"]	["EFTA00437131"]
607	Jeffrey Epstein	Peter Thiel	35	2014-09-12	2014-09-12	35	0	["Re: see you at 5 , bill burns will be here then dinner with woody and kathy On Fri, Sep 12, 2014 at 2:02 AM, Peter Thiel < > wrote:", "Re: done , see you then On Thu, Jun 5, 2014 at 5:56 PM, Peter Thiel < > wrote: maybe 8pm? Sent from my iPad On Jun 5, 2014, at 9:25 PM, \\"jeffrey E.\\" <jeevacation@gmail.com<mailtojeevacation@gmail.com>", "Re: done , see you then On Thu, Jun 5, 2014 at 5:56 PM, Peter Thiel < > wrote: maybe 8pm? Sent from my iPad On Jun 5, 2014, at 9:25 PM, \\"Jeffrey E.\\" <jeevacation@gmail.com<mailtojeevacation@gmail.com>", "Re: done , see you then On Thu, Jun 5, 2014 at 5:56 PM, Peter Thiel < > wrote: maybe 8pm? Sent from my iPad On Jun 5, 2014, at 9:25 PM, \\"Jeffrey E.\\" <jeevacation@gmail.com<mailto:jeevacation@gmail.com", "Re: Friday good On Mon, Aug 14, 2017 at 1:07 AM Jeffrey E. leevacation\\u00ae,)gmail.com> wrote: Sat On Sun, Aug 13, 2017 at 9:37 PM Peter Thiel < > wrote: Probably can't get there before Thursday... How lo"]	["EFTA00368254", "EFTA02467463", "EFTA02356637", "EFTA02060458", "EFTA00835369", "EFTA02104388", "EFTA02097825", "EFTA01008117", "EFTA01008059", "EFTA00456651"]
608	Brice Gordon	Lesley Groff	1	\N	\N	0	1	["Re: Jeffrey Epstein Super. I will have Karen and Brice get back to you! Sent from my iPhone On Aug 4, 2014, at 7:42 PM, David Smith"]	["EFTA00365490"]
609	Darren Indyke	Larry Visoski	5	\N	\N	0	5	["Fwd: [External] Epstein charter confirmed mailto: To all, Ref: Epstein S76 charter July 26, 2014 10:00am local departure from West Side NYC heli pad.,to South Hampton Beach heli pad., Gregory, AAG", "LOI Thomas World AirWays, LLC update Sony Claire Use this LOI, found a typo on previous form, PIs confirm receipt Best regards, Lany Created with Scanner Pro EFTA00664718", "Fwd: New Escrow Hello Claire,", "WI signed Thomas World Airways, LLC Dear Claire, Please find attached LOI signed, Please confirm receipt Best Regards, Larry Visoski Created with Scanner Pro Royal Jet LLC P. O. Box: 60666 Abu Dhabi U"]	["EFTA00817938", "EFTA00818820", "EFTA00366373", "EFTA00664717", "EFTA00817841"]
610	Larry Visoski	Lesley Groff	13	\N	\N	5	8	["Re: Bahamas Demmo Hello John, Can we set up the boat demo in Freeport Bahamas for June 22 late afternoon? 5pm ish Mr. Epstein is requesting demo for this date, if you can accommodate thank you let me ", "Re: Bahamas Demmo Hello John, Can we set up the boat demo in Freeport Bahamas for June 22 late afternoon? 5pm ish Mr. Epstein is requesting demo for this date, if you can accommodate thank you let me ", "Re: SAFE Boat Bahamas Demo Hello John At this time, we have a schedule conflict for June 1st, so this date is not going to work for Mr. Epstein, he has indicated possibly later in June, -will there be", "Re: Jeffrey Epstein Hi Greg...come to the house! That will be perfect. Jeffrey has changed wheels up time from Teterboro to", "Re: Wheels up >>> >>>"]	["EFTA00387218", "EFTA00369226", "EFTA00391405", "EFTA02065367", "EFTA02089646", "EFTA00368121", "EFTA00527213", "EFTA00368104", "EFTA00371338", "EFTA00385084"]
611	Brock Pierce	Lesley Groff	3	\N	\N	2	1	["Re: Jeffrey Epstein", "Re: Jeffrey Epstein", "Re: Jeffrey Epstein Brock, Jeffrey is asking your official position in the Chinese game board...possibly, could you send some information to him via email? Lesley On Thu, Sep 15, 2011 at 12:34 PM, Bro"]	["EFTA00428081", "EFTA00368862", "EFTA00368928"]
612	Eva Dubin	Lesley Groff	3	2019-04-08	2019-04-08	1	2	["Re: Eva, we have a studio apt available for your friend starting Friday May 16th...can you please let me know her full name? She may stay in ..also, once you know how long she will stay, please let me", "Re: Eva, we have a studio apt available for your friend starting Friday May 16th...can you please let me know her full name? She may stay in ..also, once you know how long she will stay, please let me", "Re: Jeffrey Epstein"]	["EFTA02283000", "EFTA00369152", "EFTA00369155"]
613	George Church	Lesley Groff	7	2016-02-02	2016-02-02	1	6	["Re: Jeffrey Epstein", "Jeffrey EPs HI George...just circling back re Jeffrey meeting up with Luhan and Geoff on Friday at Martin's institute...) would love to confirm 3pm for thcm...would it be better if I contacted them di", "Re: Jeffrey", "Jeffrey EPs ein HI George...just circling back re Jeffrey meeting up with Luhan and Geoff on Friday at Martin's institute...I would love to confirm 3pm for them...would it be better if I contacted the", "Jeffrey EPstein HI George...just circling back re Jeffrey meeting up with Luhan and Geoff on Friday at Martin's institute...I would love to confirm 3pm for them...would it be better if I contacted the"]	["EFTA00370883", "EFTA02119699", "EFTA02059410", "EFTA02059787", "EFTA02059759", "EFTA02150071", "EFTA02059593"]
614	Darren Indyke	Martin Weinberg	2	2009-04-24	2009-04-24	1	1	["Re: Opinion from 11th Circuit attached Let's have a call first thing on Monday. Please let", "Re: CMA-Amicus Curiae Bob and Rita I don't know whether your research has provided answers to any of the following issues that were \\"instigated\\" by the Jane Doe 101 filing: I) Whether 2255 was intende"]	["EFTA00774250", "EFTA00370981"]
615	Jeffrey Epstein	Tom Pritzker	80	2013-01-04	2013-01-04	70	10	["gates canceled the 14th , i have mit guys coming instead woudl love to catch up *********************************************************** The information contained in this communication is confident", "Fwd: Re:", "Re: yes 0800 fine On Mon, Jan 6, 2014 at 6:44 PM, Pritzker, Tom", "is going on an asian exploration first to bali and then kuaa lumpur and tokyo., can you help her the last two places. ? please note The information contained in this communication is confidential, may", "is going on an asian exploration first to bali and then kuaa lumpur and tokyo., can you help her the last two places. ? please note The information contained in this communication is confidential, may"]	["EFTA00373487", "EFTA00540666", "EFTA00472432", "EFTA00540736", "EFTA00838558", "EFTA00376714", "EFTA00472314", "EFTA00540739", "EFTA00625566", "EFTA00540826"]
616	Erika Kellerhals	Lesley Groff	9	\N	\N	1	8	["Re: Does JEE have time to talk to me this afternoon Erika, Jeffrey can speak this afternoon...did you want to give a window of time for the call? On Dec 13, 2013, at 10:53 AM, Erika Kellerhals Or Mond", "Re: Meeting", "Re: Meeting today", "Re:", "Re: Jeffrey's schedule Erika, Thursday works...would 2pm at STC be good? On Mar 7, 2017, at 9:16 AM, Erika Kellerhals wrote: Hi Lesley \\u2014 any chance you can get me on Jeffrey's schedule on Thursday or "]	["EFTA02071569", "EFTA00378070", "EFTA00394252", "EFTA02071232", "EFTA02207446", "EFTA02071209", "EFTA00446769", "EFTA00394404", "EFTA00439568"]
617	Darren Indyke	Erika Kellerhals	6	\N	\N	3	3	["Fwd: Submission for B&I Eva Andersson Dubin David Mitchell Joseph Pagano", "Here are final articles and plan", "while Jeffrey is signing things", "Re: Privileged and Confidential Directors are: Jeffrey Epstein Richard Kahn Darren Indyke Officers are: Pres: Jeffrey Epstein Secy: Darren Indyke Treas: Richard Kahn", "Re:"]	["EFTA00393575", "EFTA01055600", "EFTA00393573", "EFTA00433955", "EFTA00439568", "EFTA00378519"]
786	Barnaby Marsh	Deepak Chopra	3	\N	\N	2	1	["Re: Lunch yes--God is an unfortunate term -with many interpretations. For me God i= the ground of being as pure consciousness--", "Re: Science and reality Nice. The questions could be answered if the approach and =ssumptions are at the right breadth and scale; lets"]	["EFTA02458577", "EFTA01785434", "EFTA02336631"]
618	Erika Kellerhals	Jeffrey Epstein	64	2016-11-04	2018-12-07	19	45	["Submission for B&I >, Cecile , \\"Jeanne Brennan\\" Good morning. Attached is the draft submission which we need to submit in order to get the permit for the IBE. Once we have the permit \\u2014 we will formall", "Submission for B&I Good morning. Attached is the draft submission which we need to submit in order to get the permit for the IBE. Once we have the permit \\u2014we will formally incorporate the entity and p", "Re:", "Re: spoke with Rohrlick", "Re: Your call 2 On Mon, Aug 15, 2016 at 8:34 AM, Erika Kellerhals"]	["EFTA01737944", "EFTA01029038", "EFTA00378528", "EFTA00378537", "EFTA00820870", "EFTA01143512", "EFTA00964369", "EFTA01187266", "EFTA00951821", "EFTA01018558"]
619	Cecile de Jongh	Erika Kellerhals	7	\N	\N	2	5	["Submission for B&I Good morning. Attached is the draft submission which we need to submit in order to get the permit for the IBE. Once we have the permit \\u2014we will formally incorporate the entity and p", "Re: Permits Good morning JP and Michele,", "Meeting on Friday", "Re: activity on great st. james Good afternoon JP. I just received your email as I am attending a class at Northwestern. I will look into this and get back to you. I'll need to talk with Mr. Epstein b", "Meeting on Friday"]	["EFTA02518463", "EFTA01739030", "EFTA00814205", "EFTA02670966", "EFTA01063287", "EFTA01783348", "EFTA00378537"]
620	Jeffrey Epstein	Richard Branson	38	2016-06-10	2016-06-10	16	22	["plans? to\\u2022 **********\\u2022 \\u2022 ********** fri\\u2022 \\u2022 *Ho ********* \\u2022 **********\\u2022 \\u2022 \\u2022 The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside inf", "plans? I Skype me: I Tweet The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of th", "RE: Dear Jeffrey, I Thanks so much for remembering. I'll copy your email to Rob Aquadro who is overseeing the rebuild. Could you possibly let us know what equipment you've got?", "RE: Dear Jeffrey,", "RE: Dear Jeffrey,"]	["EFTA01839692", "EFTA00931476", "EFTA00931459", "EFTA00718984", "EFTA01840374", "EFTA00919380", "EFTA00931437", "EFTA00918378", "EFTA00977245", "EFTA00378890"]
621	Jeffrey Epstein	Josh Harris	3	2013-11-12	2013-11-12	3	0	[]	["EFTA02519317", "EFTA00379820", "EFTA00379826"]
622	David Mitchell	Lesley Groff	12	\N	\N	5	7	["Re: <no subject> Sent from my iPhone On Sep 25, 2013, at 6:58 PM, David Mitchell < wrote: What is Rich K email PLEASE NOTE NEW ADDRESS: DAVID MITCHELL Mitchell Holdings LLC 801 MADISON AVENUE New York", "Re: <no subject> Sent from my iPhone On Sep 25, 2013, at 6:58 PM, David Mitchell < wrote: What is Rich K email PLEASE NOTE NEW ADDRESS: DAVID MITCHELL Mitchell Holdings LLC 801 MADISON AVENUE New York", "RE: Peter Mandelsohn Dear Lesley please meet Emily Emily is mission control for Todd Boehly ,Emily please confirm with Both Lesley and I if this could work Thank you so much, David DAVID MITCHELL Mitc", "Re: Tour tomorrow at 4pm", "RE: Jeffrey Epstein"]	["EFTA01855200", "EFTA00428124", "EFTA00382495", "EFTA02251080", "EFTA01855120", "EFTA02230745", "EFTA02230756", "EFTA00901960", "EFTA00382830", "EFTA02230751"]
623	Greg Wyler	Larry Visoski	2	\N	\N	2	0	["Dinner I Skype me Jeffrey would be delighted to stay for dinner. I will let him give you some feedback on the guests and", "Dinner I Skype me: Jeffrey would be delighted to stay for dinner. I will let him give you some feedback"]	["EFTA00384070", "EFTA02130162"]
624	Jeffrey Epstein	John Brockman	11	2015-07-10	2015-07-10	4	7	["Fwd: save the date", "Fwd: save the date", "Re: Bjorn Lomberg", "Re: Gary Rosen tomorow or on the 31 On Thu,  Jan 20, 2011 at 9:42  PM, Rosen Ga mailto <mailto: <mailto: \\u00bb wrote: Same here. Got any plans to be in NYC soon?", "Re:"]	["EFTA00968898", "EFTA01206030", "EFTA00905014", "EFTA00384553", "EFTA02715990", "EFTA01791745", "EFTA00384562", "EFTA02130386", "EFTA00714517", "EFTA01961612"]
625	Bill Gates	Jeffrey Epstein	23	\N	\N	9	14	["Possible dinner in New York..", "Possible dinner in New York..", "Possible dinner in New York..", "Re: Re:", "Possible dinner in New York.."]	["EFTA01142883", "EFTA00986219", "EFTA00977539", "EFTA00966909", "EFTA01964544", "EFTA00975619", "EFTA00975091", "EFTA01003196", "EFTA00706624", "EFTA01962824"]
626	Erika Kellerhals	Richard Kahn	6	2014-09-11	2016-11-04	4	2	["Re: issues for conference call I'll be unavailable for the next few hours so please coordinate with my assistant Gina at", "Re: Southern Trust", "Re: Southern Trust", "Re: Democratic clubs in STT & STX", "Re: Fyi We do want to have =ialogue however you put us in a system that never worked properly from"]	["EFTA01737944", "EFTA02606268", "EFTA02607857", "EFTA00710987", "EFTA00385812", "EFTA01192582"]
627	Boris Nikolic	Jeffrey Epstein	680	2009-11-12	2017-03-25	27	653	["Sam wants to stay in the upstairs guest apt in Paris . Please coordinate with Valddon starting wed The information contained in this communication is confidential, may be attorney-client privileged, m", "Sam wants to stay in the upstairs guest apt in Paris . Please coordinate with Valddon starting wed The information contained in this communication is confidential, may be attorney-client privileged, m", "Sam wants to stay in the upstairs guest apt in Paris . Please coordinate with Valddon starting wed The information contained in this communication is confidential, may be attorney-client privileged, m", "> wrote: Sam wants to stay in the upstairs guest apt in Paris . Please coordinate with Valddon starting wed The information contained in this communication is confidential, may be attorney-client priv", "looking forward to spending time *********************************************************** The information contained in this communication is confidential, may be attorney-client privileged, may con"]	["EFTA00421840", "EFTA00648334", "EFTA00638950", "EFTA00648339", "EFTA00406711", "EFTA00629010", "EFTA00389977", "EFTA00431647", "EFTA00648266", "EFTA00389981"]
628	Jeffrey Epstein	Michael Wolff	6	\N	\N	2	4	["Re: Jeffrey Epstein/photo Marvin--I'm cc Jeffrey here who is expecting to hear from you about a photo shoot. I understand from Jeffrey who is in NYC now that he is leaving today (at 2:001 think), and ", "Re: Jeffrey Epstein/photo Marvin-.I'm cc Jeffrey here who is expecting to hear from you about a photo shoot. I understand from Jeffrey who is in NYC now that he is leaving today (at 2:00 I think), and", "look at this...", "Re: Jeffrey Epstein/photo Marvin\\u2014I'm cc Jeffrey here who is expecting to hear from you about a photo shoot. I understand from Jeffrey who is in NYC now that he is leaving today (at 2:001 think), and b", "walk in park around 1230. hot dog /lunch? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only fo"]	["EFTA00391075", "EFTA00861082", "EFTA00865018", "EFTA00709854", "EFTA02140214", "EFTA00632637"]
644	Bella Klein	Darren Indyke	31	2014-06-23	2016-03-21	28	3	["Re: Chairs at the Gotham Awards", "Re: Chairs at the Gotham Awards", "NES WT to Tes EFTA01401456", "NES WT to Tes Amanda, Please confirm wire Thank you, Bella Tel: Begin forwarded message: EFTA01401530", "JEE WT"]	["EFTA01404610", "EFTA01401455", "EFTA01413940", "EFTA01412104", "EFTA01405911", "EFTA00439562", "EFTA01413709", "EFTA01411912", "EFTA01401771", "EFTA01402554"]
629	Caroline Lang	Darren Indyke	4	\N	\N	0	4	["Draft Agreement Dear Caroline, P' I wanted to make sure that you received the email below and find out when I can expect to receive the draft", "Draft Agreement Dear Caroline, I> I wanted to make sure that you received the email below and find out when I can expect to receive the draft", "Draft Agreement Dear Caroline, I wanted to make sure that you received the email below and find out when I can expect to receive the draft", "Draft Agreement Dear Caroline, PI I wanted to make sure that you received the email below and find out when I can expect to receive the draft"]	["EFTA00392259", "EFTA00958888", "EFTA00958882", "EFTA00958876"]
630	Jeffrey Epstein	Peggy Siegal	127	\N	\N	97	30	["Re: Fwd: Fw: Annette Siegal's estate", "Re: Stuck at office.. Why does she ask about me single On Wednesday, December 5, 2012, Jeffrey Epstein wrote: I'm in Paris On Wednesday, December 5, 2012, Peggy Siegal wrote: Come to the party...see A", "peggy was going to send us a list of events. tonite. throught the 15th. . thanx please note The information contained in this communication is confidential, may be attorney-client privileged, may cons", "anything sun or mon '? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the u", "70th Birthday Dinner in Southampton Dear Jeffrey, As you know, I am in the South of France finishing up the last leg of my three week trip to London, Capri,"]	["EFTA00700955", "EFTA00673450", "EFTA00712229", "EFTA00393677", "EFTA00647154", "EFTA00456474", "EFTA00400091", "EFTA00700276", "EFTA00440198", "EFTA00661329"]
631	Andrew Farkas	Richard Kahn	1	\N	\N	1	0	["AYH Discussion"]	["EFTA00393879"]
632	Boris Nikolic	Lesley Groff	3	\N	\N	0	3	["Jeffrey Epstein Hello Boris. Hope you are doing well!! Could you please provide me the following information for both you and Sam? Full Name as it appears on your Passport Company Address Phone number", "Jeffrey Epstein Hi Boris...Jeffrey would like to speak with you when you when you have a minute. Could you please give him a call at Thanks, Lesley EFTA00433585", "Re: RE: EFTA_R1_00787497 EFTA02137525"]	["EFTA00394973", "EFTA00433584", "EFTA02137524"]
633	Boris Nikolic	Kimbal Musk	9	2012-09-21	2012-09-21	0	9	["Invites for tomorrow night Hey! Fun time last night! Let Jeffrey and his friends know they are invited tomorrow night. Four Seasons. 7pm. Black tie. Arrive no later", "Invites for tomorrow night Hey! Fun time last night! Let Jeffrey and his friends know they are invited tomorrow night. Four Seasons. 7pm. Black tie. Arrive no later", "Fwd: Medication use higher among overweight, obese kids 2 EFTA_R1_00136821 EFTA01798705", "Invites for tomorrow night Hey! wrote: Fun time last night! Let Jeffrey and his friends know they are invited tomorrow night. Four Seasons. 7pm. Black tie. Arrive no later", "Invites for tomorrow night Hey! Fun time last night! Let Jeffrey and his friends know they arc invited tomorrow night. Four Seasons. 7pm. Black tie. Arrive no later"]	["EFTA01888239", "EFTA00944734", "EFTA01798704", "EFTA00404176", "EFTA01987495", "EFTA01888383", "EFTA01884458", "EFTA02004313", "EFTA01989291"]
634	Jeffrey Epstein	Karyna Shuliak	37	2016-11-28	2018-04-13	27	10	["Larry&Dave", "jean luc canceld *********************************************************** The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside i", "Cushions from Artefacto", "jean luc canceld *********************************************************** The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside i", "Re: Hotel Stays for Karyna! Hi Jeannine, I would like to inform you, that I have to change a few dates for my trip. I will get back to you once I have new reservations"]	["EFTA00566602", "EFTA00539522", "EFTA00529386", "EFTA00536613", "EFTA01914472", "EFTA00566607", "EFTA01050141", "EFTA00406998", "EFTA02299706", "EFTA00541229"]
635	Jeffrey Epstein	Tim Zagat	3	\N	\N	3	0	[]	["EFTA01769845", "EFTA00412244", "EFTA00543281"]
636	Jeffrey Epstein	Paul Morris	52	2013-10-09	2015-01-12	51	1	["Re: Follow-up", "Re: FW: Longer Dated EUR Downside (3y structures) [CJ", "Re: just typing you an eaill , lets do a total return swap 250,000 apple On Fri, Jan 8, 2016 at 3:50 PM, Paul Morris < wrote: Hope you're well let's find few minutes to connect early next week. Thanks", "Re: DB James Malcolm: Are the B03 shifting stance? Own some cheap optionality send me put and calls at different strikes and duration, why in the world would i put up any money if i can short puts ? b", "Re: Call follow-ups [CJ"]	["EFTA01193579", "EFTA01404139", "EFTA01193576", "EFTA00715644", "EFTA01401348", "EFTA00903307", "EFTA00852795", "EFTA00637540", "EFTA00639961", "EFTA00632114"]
637	Lawrence Krauss	Noam Chomsky	20	\N	\N	20	0	["Re: Xenophobia in April You didn't answer about meeting Epstein. I can understand if you can't or don't want to but of you can let me", "Re: Xenophobia In April If you are willing Is there anyone I can have him contact to set up an appointment?", "Re: Xenophobia in April You didn't answer about meeting Epstein. I can understand if you can't or don't want to but of you can", "Re: Xenophobia in April You didn't answer about meeting Epstein. I can understand if you can't or don't want to but of you can let me", "Re: Xenophobia In April If you are willing Is there anyone I can have him contact to set up an appointment?"]	["EFTA02476406", "EFTA02486016", "EFTA00416073", "EFTA00660418", "EFTA01800759", "EFTA01793968", "EFTA01793988", "EFTA01870502", "EFTA00416065", "EFTA01993967"]
638	Dana	Lesley Groff	1	\N	\N	0	1	["Re: GM"]	["EFTA00418507"]
639	Jeffrey Epstein	Matthew I. Menchel	72	\N	\N	72	0	["do you have your new york dates yet.? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for th", "do you have your new york dates yet.? **4g######################################################## The information contained in this communication is confidential, may be attorney-client privileged, m", "Re: wrote: your name just came up\\u201e when you sent an email to weingarten \\u201e he is with me in paris love to see you On Wed, Sep 28, 2011 at 11:39 PM, Matthew I. Menchel < > wrote: Long time, no speak. Ho", "Re: thurs? On Mon, Oct 31, 2011 at 8:00 PM, Matthew I. Menchel < > wrote: Be in New York starting tomorrow and will be there for the next 3 weeks. This week would be best because once I", "if i come to florida would you have time on the 15 **4g######################################################## The information contained in this communication is confidential, may be attorney-client "]	["EFTA00920762", "EFTA00740708", "EFTA00868609", "EFTA00753954", "EFTA00923615", "EFTA00923570", "EFTA00671022", "EFTA00661279", "EFTA00697115", "EFTA00959395"]
640	Jay Lefkowitz	Jeffrey Epstein	2	2011-08-08	2011-08-08	0	2	["Re: Epstein I", ">; Darren I seems more than a little odd, that my lawyers in florida, take over a complaint from critten, then file and amended complaint. , in the beginning telling me that we have to bolster damages"]	["EFTA00429389", "EFTA00917539"]
641	Lesley Groff	Martin Weinberg	1	\N	\N	1	0	["Re: Jeffrey Epstein"]	["EFTA00435432"]
645	Dick Cavett	Lesley Groff	2	\N	\N	0	2	["Jeffrey Epstein Good morning Lisa...just checking in to see how the detailed budget is coming along for Jeffrey...could you let me know when he can expect this? Thank you! Lesley Assistant to Jeffrey ", "Re: Jeffrey Epstein Morning Lisa! Hope all is well...following up on the budget for JE...might they have something to share with him as of yet? On Jan 11, 2017, at 1:52 PM, Lisa Troland wrote: Hi Lesl"]	["EFTA00443254", "EFTA00442945"]
646	Deepak Chopra	Janusz Banasiak	7	\N	\N	7	0	["Re: Jeffrey Epstein Ok Great I may not be done filming until 4 PM but will stay in touch My cell is Deepak Chopra MD 2013 Costa Del Mar Road Carlsbad,  CA 92009 Chopra Foundation Ji3o", "Re: Jeffrey Epstein Perfect Will stay in touch and come early when done at PBS Deepak Chopra MD Carlsbad,  CA 92009 Chopra Foundation Jiyo Chopra Center for Wellbeing EFTA00458178", "Re: Jeffrey Epstein Perfect Will stay in touch and come early when done at PBS EFTA00458939", "Re: Jeffrey Epstein Perfect Will stay in touch and come early when done at PBS Deepak Chopra MD Chopra Foundation liyo Chopra Center for Wellbeing EFTA01029668", "Re: Jeffrey Epstein Perfect Will stay in touch and come early when done at PBS Deepak Chopra MD Chopra Foundation Jiyo Chopra Center for Wellbeing EFTA01029684"]	["EFTA01029667", "EFTA00458938", "EFTA00458177", "EFTA02205067", "EFTA00444334", "EFTA02222792", "EFTA01029683"]
647	Deepak Chopra	Jeffrey Epstein	184	\N	\N	11	173	["Re: Note To jE Yes and if you want to stay sat Ivan have you driven back for sun morning Either way see you sat On Mon, Feb 6, 2017 at 3:05 PM Deepak Chopra l> wrote: Please listen 1 min Let me know p", "viome? EFTA00474583", "Re: Tomorrow, Tuesday? On Sun, Jun 17, 2018 at 3:19 PM Deepak Chopra < Yes Just got back from Omega Deepak Chopra MD 2013 Costa Del Mar Road Carlsbad, CA 92009 Chopra Foundation LY0 Apra Center for We", "now where? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the ad", "Re: how does propanfanol, effect conciousness? mechanism? On Mon, Oct 10, 2016 at 7:40 AM, Deepak Chopra I> wrote: I'm in and out all week Have a busy day Wed and Friday And a quick 2 trips to Boston "]	["EFTA00691562", "EFTA00658325", "EFTA00690888", "EFTA00697111", "EFTA00813274", "EFTA00641324", "EFTA00474582", "EFTA00634870", "EFTA00476452", "EFTA00634880"]
648	Deepak Chopra	Lesley Groff	10	\N	\N	1	9	["Jeffrey Epstein Hello Deepak...Jeffrey would like to send you a DNA test..can you please provide an address that we may send this to?", "Re: Jeffrey Epstein Perfect Will stay in touch and come early when done at PBS EFTA00458939", "Jeffrey Epstein 12:00pm! > Morning Deepak. Reconfirming you will come see Jeffrey today, Friday June 8th, at noon for lunch! 9 East 71st Street between 5th and Madison Thanks! Lesley Assistant to Jeff", "Re: Jeffrey Epstein OK...sounds good..will wait to hear back On Aug 20, 2018, at 11:15 AM, Deepak Chopra wrote: Most probably yes Will confirm today Deepak Chopra MD 2013 Costa Del Mar Road Carlsbad C", "Re: Jeffrey Epstein Oh yes!!! For sure! 2pm wed at Jeffreys house. I confirmed earlier! Hopefully I replied all?! 9 East 71st"]	["EFTA02191605", "EFTA00458938", "EFTA00476301", "EFTA02234292", "EFTA00445294", "EFTA00480395", "EFTA02204313", "EFTA02561917", "EFTA00480419", "EFTA00480371"]
649	Jeffrey Epstein	Lawrence Krauss	38	\N	\N	9	29	["Re: Fun coordinate with lesley On Thu, Jul 6, 2017 at 7:50 PM, Lawrence Krauss wrote:", "Re: Fun coordinate with lesley On Thu, Jul 6, 2017 at 7:50 PM, Lawrence Krauss < > wrote:", "Re: Fun coordinate with lesley On Thu, Jul 6, 2017 at 7:50 PM, Lawrence Krauss < wrote:", "hi", "Re: Re. Peter Rillero"]	["EFTA00758048", "EFTA00681134", "EFTA01020499", "EFTA01022516", "EFTA01800759", "EFTA01793968", "EFTA00897256", "EFTA01793988", "EFTA00779017", "EFTA00752531"]
650	Jesse	Lesley Groff	3	\N	\N	0	3	["Re: Meeting with JE", "Re: Meeting with JE", "Re: Meeting with JE"]	["EFTA00460666", "EFTA00461585", "EFTA00460661"]
651	Bella Klein	Larry Visoski	1	\N	\N	0	1	["Re: Chater request *** CAUTION - EXTERNAL EMAIL ' Hello Brad and Heliflite We had to cancel today flight due to Illness of the lead passenger We wire Trafr the invoice\\u201e What is cancellation policy? Sh"]	["EFTA00461188"]
652	Larry Summers	Lesley Groff	2	2018-02-09	2018-11-25	0	2	["Jeffrey Epstein", "Jeffrey Epstein > > <mailto:sarah@lawrencesummers.com\\u00bb, Hello= andIMI! Hope you both had a tre=endous Thanksgiving...Jeffrey will be in NY end of this week =A6looks like they are trying to coordinate "]	["EFTA02615143", "EFTA00469107"]
653	Lesley Groff	Masha Drokova	1	2018-03-29	2018-03-29	0	1	["Re: Haircut w/Patrick at Fekkai Salon Fri. March 30! Super. Will be there by 4 On Mar 29, 2018, at 10:11 PM, Lesley Groff Ok. Sounds bad good Sent from my iPhone On Mar 29, 2018, at 9:36 PM, Masha Dro"]	["EFTA00471932"]
654	David Mitchell	Richard Kahn	15	2017-07-21	2019-03-04	10	5	["Re: NYC contractor", "Fwd: Art Moving Authorization", "Fwd: Art Moving Authorization", "Re: NYC contractor", "Re: NYC contractor"]	["EFTA00570492", "EFTA00472980", "EFTA00570502", "EFTA01018745", "EFTA02377090", "EFTA02456374", "EFTA02245899", "EFTA02632931", "EFTA01017198", "EFTA01058407"]
655	Brad Karp	Lesley Groff	5	\N	\N	0	5	["Jeffrey Epstein HI Brad. Nice to see you today! Jeffrey says you were to deliver something to him by hand...just checking to see", "Jeffrey Epstein", "Jeffrey Epstein > wrote:", "Jeffrey Epstein", "Jeffrey Epstein Hello Brad. Reconfirming you will come see Jeffrey tonight for dinner at 7pm 9 East 71st Street between 5th and Madison Thank you, Lesley Assistant to Jeffrey Epstein This message is i"]	["EFTA02531843", "EFTA00483556", "EFTA00476384", "EFTA02261918", "EFTA00483554"]
656	Eva Dubin	Jeffrey Epstein	12	2016-05-01	2018-06-27	7	5	["Paris", "Paris", "Paris", "eva is on the daldry case\\u201e she is raising money for the mount sinai dubin breast cancer center\\u201e lets have a movie screening, to benefit the center\\u201e i will sponsor. please coordinate with Eva The infor", "RE:"]	["EFTA00740178", "EFTA02356320", "EFTA01793355", "EFTA02178078", "EFTA00770921", "EFTA02052018", "EFTA02512117", "EFTA00477343", "EFTA00477333", "EFTA01789875"]
657	Carluz Toylo	Jeffrey Epstein	2	2018-07-18	2018-07-18	0	2	[]	["EFTA00478750", "EFTA00478582"]
658	Jeffrey Epstein	Lisa Randall	12	2014-11-29	2014-11-29	7	5	["Re: Fwd: Lisa Randall", "Re: at last ------ On Mon, Aug 16, 2010 at 12:47 PM, Lisa Randall <", "good time? *** ************************************** ****************** The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside infor", "Re: at last ----- On Mon, Aug 16, 2010 at 12:47 PM, Lisa Randall < Free ? Sent from my iPhone On May 8, 2010, at 11:17 AM, Jeffrey Epstein <jcevacationtegmail.com> wrote: can you give me a call ******", "Re: at last On Mon, Aug 16, 2010 at 12:47 PM, Lisa Randall <"]	["EFTA02089189", "EFTA01980329", "EFTA02434255", "EFTA00767779", "EFTA02300610", "EFTA00896049", "EFTA01780767", "EFTA02089073", "EFTA00896041", "EFTA00532046"]
787	Jeffrey Epstein	Kimbal Musk	1	\N	\N	0	1	["Fwd: Medication use higher among overweight, obese kids 2 EFTA_R1_00136821 EFTA01798705"]	["EFTA01798704"]
659	Bella Klein	Karyna Shuliak	18	2016-03-09	2017-06-23	9	9	["Re: JSC Interiors here is the form krtelacto inex authorization 05/26/16 EFTA00533520", "Re: and Karyna Shuliak", "Re: Outdoor furniture order O(20180118 Dear Kiko, Please clarify your last email. I am not sure why you are confirming payment receipts on March 26th when my bank confirmed wire transfer on March 19th", "Re: LSJ kitchen fabric Seth said he can have it shipped directly to St. Thomas On Jul 25, 2018, at 2:24 PM, Bella Klein < > wrote: Daphne, I believe fedex should go to Tropical not to VI. Please confi", "Re: LSJ kitchen fabric Daphne, Please take over the shipping. You are the best at it! Thank you, Bella Tel: On Jul 25, 2018, at 3:11 PM, Karyna Shuliak"]	["EFTA00540362", "EFTA00546020", "EFTA02301157", "EFTA00575066", "EFTA02323988", "EFTA00567265", "EFTA00553374", "EFTA00575064", "EFTA02309549", "EFTA00567215"]
660	Daphne Wallace	Karyna Shuliak	24	\N	\N	15	9	["Mattress order EXT MSG: Hi Judy, This is Karyna. As per our conversation, I included Ms.Daphne Wallace on this email, who will be able to", "Re: duc duc beds - product info + pricing Hi Kathryn,", "Re: duc duc beds - product info + pricing Dear Kathryn, I have copied Mrs. Daphne Wallace on this email. She is coordinating the shipping process and will be able to assist", "Re: duc duc beds - product info + pricing Thank you! On Mar 27, 2018, at 12:14 PM, Kathryn Magagna", "Re: 4 rugs Dear Mo, I haven't heard back from you regarding the rugs. You mentioned that you were going to receive them on"]	["EFTA00546020", "EFTA00548650", "EFTA00571214", "EFTA00546553", "EFTA00552552", "EFTA00546970", "EFTA00546547", "EFTA00547656", "EFTA00544616", "EFTA00552397"]
661	Karyna Shuliak	Richard Kahn	33	2014-05-30	2018-03-12	18	15	["Re: ESTIMATE Curtain divider for 11P Yes On Tue, Jun 20, 2017 at 1:33 PM Karyna Shuliak < > wrote: Jeffrey, Regarding the curtain divider for another studio apartment: Rich spoke with the company, the", "Re: ARTEFACTO- Rug Exchange confirming delivery time is ok for august 3rd from 9-I lam please have men ask for susan who will accept carpet and assist with pickup thank you Richard Kahn", "Re: Artefacto - aditional items PB / REVIEW Manilla On Feb 2, 2015, at 1:36 PM, Karyna Shuliak < wrote: Thank you Eduardo! We still need another 2 coffee tables with the cushions. Could you please pla", "Re:", "Re: Your order from ducduc Shipped! eileen i just left you a voicemail waiting until July 4th is not acceptable"]	["EFTA00534758", "EFTA00574491", "EFTA00564939", "EFTA00570572", "EFTA00567265", "EFTA00575357", "EFTA00536993", "EFTA00551935", "EFTA00573857", "EFTA00535981"]
662	Bella Klein	Daphne Wallace	21	\N	\N	3	18	["Re: Outdoor furniture order O(20180118 Dear Kiko, Please clarify your last email. I am not sure why you are confirming payment receipts on March 26th when my bank confirmed wire transfer on March 19th", "Re: LSJ kitchen fabric Daphne, Please take over the shipping. You are the best at it! Thank you, Bella Tel: On Jul 25, 2018, at 3:11 PM, Karyna Shuliak", "Re: Shipment La to ST Thomas c yen e ma atrans\\u2022 Greetings Gusti and Rina,", "Re: Shipment La to ST Thomas c/Karyna Shuliak Greetings, When can we expect to get information on the arrival date of our shipment? Please advise if there is a confirmed", "Re: Shipment La to ST Thomas c/Karyna Shuliak Greetings, When can we expect to get information on the arrival date of our shipment? Please advise if there is a"]	["EFTA00547003", "EFTA00547959", "EFTA00547908", "EFTA00548650", "EFTA00548388", "EFTA00546553", "EFTA00540362", "EFTA00546970", "EFTA00546547", "EFTA00547656"]
663	Bella Klein	Valdson Cotrin	5	2016-06-29	2016-06-29	2	3	["Visit JE will be going to Paris around May 10...Please make sure the phones are up and running and everything is in", "Visit JE will be going to Paris around May 10...Please make sure the phones are up and running and everything is", "Re: rdv fibre optique Marie-Joseph Experton ok tmne bella je ferais le n\\u00e9cessaire pour que victor de la compagnie isc entre en contacte avec james mercredi 15", "Re: rdv fibre optique Marie-Joseph Experton ok tnme bella je ferais le n\\u00e9cessaire pour que victor de la compagnie isc entre en contacte avec james mercredi 15 avril", "Fwd: Paris - Palm Beach"]	["EFTA00540387", "EFTA00540876", "EFTA00859406", "EFTA00716826", "EFTA02458800"]
664	Brice Gordon	Karyna Shuliak	9	\N	\N	4	5	["Re: LSJ Cabana Tiles As requeste, attached shipping information On Tue, Jul 31, 2018 at 11:39 AM, Molly S. Roberg < Hi Brice,", "Re: Artistic Tile Thassos Hi Molly,", "Re: Artistic Tile Thassos Hi Molly,", "Re: Artistic Tile Thassos Hi Molly,", "Re: Artistic Tile Thassos Good afternoon Molly Payment has been processed Would it be possible to country of origin added to invoice It is a Customs requirement for all shipments to the USVI regards B"]	["EFTA02309081", "EFTA02344412", "EFTA00546190", "EFTA00547088", "EFTA00547098", "EFTA02309958", "EFTA02311179", "EFTA00547102", "EFTA00547113"]
665	Brice Gordon	Daphne Wallace	5	\N	\N	2	3	["[EXT] Re: JSC Interiors LLC - Bid No. B988933 - July 24, 2018 Greetings Ryan, ; LSJ GSJ As promised, I would like for you to ship out as soon as possible the order that has arrived. Thank you for havi", "=wd: SHEEHAN/CHRISTOPHER 05DEC2016 STT SJU Greetings Chris, 2 EFTA_R1_00086264 EFTA01773440", "Fwd: Quote for Hangar Painting Kern has already started work at TWA, can i please have deposit", "Fwd: Quote for Hangar Painting Kern has already started work at TWA, can i please have deposit"]	["EFTA02309535", "EFTA01773439", "EFTA00547918", "EFTA02025775", "EFTA02002249"]
666	Lesley Groff	Valdson Cotrin	10	\N	\N	10	0	["Jeffrey Epstein", "Re: RE: EFTA_R1_00787497 EFTA02137525", "Jeffrey Epstein", "Jeffrey Epstein", "Jeffrey Epstein"]	["EFTA02164538", "EFTA02165093", "EFTA02165614", "EFTA02165622", "EFTA02137524", "EFTA02164495", "EFTA00549579", "EFTA02164618", "EFTA02165313", "EFTA02165004"]
667	Bella Klein	Jeffrey Epstein	29	2015-07-23	2015-07-23	25	4	["Fwd: EPSTEIN / Devis fenetres C Attached, please find new quote from WINDOFF for 5 windows in Paris apartment. Total cost with VAT:", "Fwd: EPSTEIN / Devis fenetres C Attached, please find new quote from WINDOFF for 5 windows in Paris apartment. Total cost with VAT:", "Fwd: EPSTEIN / Devis fenetres Attached, please find new quote from WINDOFF for 5 windows in Paris apartment. Total cost with VAT:", "Fwd: EPSTEIN / Devis fenEtres Attached, please find new quote from WINDOFF for 5 windows in Paris apartment. Total cost with VAT:", "Fwd: Sony for all the typos .Sent from my iPhone Begin forwarded message:"]	["EFTA00890969", "EFTA01436304", "EFTA00851070", "EFTA01420572", "EFTA01022583", "EFTA01438609", "EFTA02342955", "EFTA00550845", "EFTA02342982", "EFTA02494379"]
668	Anthony Barrett	Richard Kahn	1	\N	\N	0	1	["Re: rent payment received from Mc2 Mode Management"]	["EFTA00552863"]
669	Bella Klein	Carluz Toylo	8	2018-05-17	2019-04-30	5	3	["Re: AED defibrillators preventative maintenance", "Re: AED defibrillators preventative maintenance", "Re: AED defibrillators preventative maintenance", "Re: Invoice 236339 from GEORGE BRITTAIN LAND DESIGNS, Inc.", "4 Pallets for service entry"]	["EFTA01033359", "EFTA02666025", "EFTA02315733", "EFTA00554406", "EFTA00554417", "EFTA01058399", "EFTA02315761", "EFTA00554853"]
788	David Mitchell	David Stern	2	\N	\N	0	2	["Re: Dubai Visit Dear Elaine,", "Re: Dubai Visit Dear Elaine,"]	["EFTA01814389", "EFTA02413153"]
792	Cecile de Jongh	Larry Visoski	1	\N	\N	0	1	["SIT ramp junk"]	["EFTA01957921"]
670	Brice Gordon	Jeffrey Epstein	33	2012-12-04	2018-06-22	19	14	["aust found out that no one has appover the various white fans\\u201e doug thought the electirican ordered, gary does know who approved.. emad didn't ask my approval or anyone else for that matter. i have no", "Re: ZDC-Broadband-T1 ok On Wed, Aug 27, 2014 at 12:15 PM, Brice Gordon <I > wrote: Sorry photo attach On Wed, Aug 27, 2014 at 10:14 AM, Brice Gordon <I I> wrote: Attached photo of proposed Verizon Ant", "Re: is this accurate Sony for the late response have got back into cell area The answer is No And who reported this? Sent from my iPhone On Dec 15, 2010, at 8:29 AM, \\"Jeffrey Epstein\\" leevacation@gmai", "LSJ PRD Refit", "David Starofsky"]	["EFTA00733714", "EFTA00751968", "EFTA01788640", "EFTA02002249", "EFTA02007970", "EFTA01059750", "EFTA00659304", "EFTA00683822", "EFTA01904411", "EFTA01202015"]
671	Emad Hanna	Jeffrey Epstein	142	2010-12-08	2010-12-08	11	131	["aust found out that no one has appover the various white fans\\u201e doug thought the electirican ordered, gary does know who approved.. emad didn't ask my approval or anyone else for that matter. i have no", "FW: Domestic Hot Water Repair 71st Street low zone. C4evel.1st 82nd Floors(secunty Upgrade.)", "Re: Mechanical Building gary has to decide it ok On Mon, Jul 27, 2009 at 11:34 AM. Emad Hanna 4:1 Jeffrey, > wrote: I just wanted you to be informed of the following:", "Re: Cell Phone ??? On Fri, Jan 7, 2011 at 12:03 PM, Emad Hanna wrote: Jeffrey, Am I keeping the company cell phone I got or am I returning it? Thank you Emad Hanna Project Controller HBRK Associates 3", "Re: Personal 15 ok On Sun, Mar 7, 2010 at 4:23 PM, Emad Hanna Jeffrey, > wrote: I really hate to ask for your assistance. I'm in need of immediate cash flow and have not been able to mount any savings"]	["EFTA00642615", "EFTA00709276", "EFTA00733416", "EFTA00648893", "EFTA00731932", "EFTA00683822", "EFTA00709265", "EFTA00685585", "EFTA00648897", "EFTA00559703"]
672	Gary Kerney	Jeffrey Epstein	143	2010-03-11	2011-11-15	35	108	["aust found out that no one has appover the various white fans\\u201e doug thought the electirican ordered, gary does know who approved.. emad didn't ask my approval or anyone else for that matter. i have no", "Re: tiki budget", "please provide me dates on which i can expect work\\u201e thanks The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is", "Re: yes to all On Thu, Mar 31, 2011 at 6:33 PM, Gary are Kernesoni wrote: I think the little office,new cabana e under control,the f elp ].pool building, the floor plan is agreed.but interior finishes", "our call will have to wait untiil rich kahn comes in tomorrow The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and"]	["EFTA00733714", "EFTA00736661", "EFTA00709276", "EFTA00682176", "EFTA00705434", "EFTA00746834", "EFTA00736014", "EFTA00559703", "EFTA00732029", "EFTA00708947"]
673	Eva Dubin	Karyna Shuliak	1	\N	\N	1	0	["Re: Extra mirror Mailable Absolutely!! Please note, my email address has changed to On May 12, 2017, at 12:48 PM, Karyna Shuliak < > wrote: Hi Eva, We have an extra standing mirror available in one of"]	["EFTA00565309"]
674	Lesley Groff	Martin Nowak	6	2016-09-14	2019-05-10	5	1	["Jeffrey Epstein", "Re: Jeffrey Thursday June 4th!!!! Hi Martin and Katherine...wanted to let you know Jeffrey is organizing a group lunch for 12:30 on Thursday June 4th...The Chomsky's and George Church are attending so", "Re: Jeffrey Thursday June 4th!!!! Hi Martin and Katherine...wanted to let you know Jeffrey is organizing a group lunch for 12:30 on Thursday June 4th...The Chomsky's and George Church are attending so", "Re: Dinner Nov. 30th From Yoki", "Re: PROJECTS Dcar Did you make progress to removing PED from the website?"]	["EFTA02287000", "EFTA02077169", "EFTA02089587", "EFTA02078253", "EFTA00572327", "EFTA02433705"]
675	Cecile de Jongh	Karyna Shuliak	1	\N	\N	0	1	["Re: VI Application for Dental Licensure > Dear Ms. Richardson, Thank you for taking the time to speak to me on the phone yesterday. I am looking forward to being approved for licensure at the next Boa"]	["EFTA00573851"]
676	Brice Gordon	Emad Hanna	8	\N	\N	5	3	["FW: Caricement Invoice- Cement purchase LSJ Mech Bldg 05.130 I don't know if you want to get JE's approval on this or not?", "Re: LSJ Approval Emad Vendor: Pro Concrete Pumping Amount: $2,780.00 The above is approved for payment Brice On 6/11/09 12:45 PM, \\"Emad Hanna\\" wrote:", "Re: is this accurate Sony for the late response have got back into cell area The answer is No And who reported this? Sent from my iPhone On Dec 15, 2010, at 8:29 AM, \\"Jeffrey Epstein\\" leevacation@gmai", "Re: Zorro fountain The most recent one On 12/22/09 7:54 PM, \\"Emad Hanna\\" alIMS wrote: > Brice, > Are you referring to the $ 2,589 payment or the most recent one you > submitted for $ 13k > Emad Hanna ", "LSJ: Lady K Emad"]	["EFTA01822727", "EFTA00666061", "EFTA00649066", "EFTA00750567", "EFTA02318588", "EFTA00610472", "EFTA02023669", "EFTA00610446"]
677	Alan Dershowitz	Martin Weinberg	2	2009-04-24	2009-04-24	1	1	["No response new from DB to multiple messages", "Re: CMA-Amicus Curiae Bob and Rita I don't know whether your research has provided answers to any of the following issues that were \\"instigated\\" by the Jane Doe 101 filing: I) Whether 2255 was intende"]	["EFTA00774250", "EFTA00629724"]
678	Daphne Wallace	Janusz Banasiak	1	\N	\N	0	1	["Re: Carpet for GSJ Hi Ann, these carpet are made to install them from wall to wall. They do not sell them by sizes, they are"]	["EFTA00632043"]
679	Nicholas Ribis	Richard Kahn	7	2018-09-09	2018-09-09	2	5	["Re: jewelry Ok. Please let me know your timing and I can meet you at 9 east 71st. Tomorrow I Will send promissory note", "Re: Promissory Note ca please let me know what time we can meet monday in addition, can you please send me today an itemized list of all jewelry you will be bring on monday thank you Richard Kahn", "Re: jewelry", "meeting any update on timing? Richard Kahn", "Re: No Sent from my iPhone On Sep 9, 2018, at 4:17 PM, Richard Kahn < please advise if i can cash check on tuesday thank you Richard Kahn"]	["EFTA02644555", "EFTA00634757", "EFTA02341757", "EFTA02623222", "EFTA02623187", "EFTA00670919", "EFTA01041559"]
680	Ben Goertzel	Richard Kahn	2	2014-12-24	2014-12-24	2	0	["Re: Hi Richard, Below is the bank information. When you've done the wire, please let me know to which account you have sent the funds and in what amount,", "Re: Hi Richard, Below is the bank information. When you've done the wire, please let me know to which account you have sent the funds and in what amount,"]	["EFTA00636933", "EFTA00673244"]
681	Jeanne Brennan Wiebracht	Jeffrey Epstein	17	\N	\N	10	7	["Re: FW: Anna's Salary yes On Fri, May 29, 2015 at 8:29 AM, Jeanne Brennan Wiebracht < wrote: ' Jeffrey", "Re: FW: Anna's Salary Yes On The, Nov 25, 2014 at 1:05 PM, Jeanne Brennan Wiebracht < Jeffrey Should I process Anna's $3000 monthly bonus for Nov? Jeanne please note The information contained in this ", "FW: FW: Anna's Salary Jeffrey Should I process Anna's $3000 monthly LSJE bonus for July ? Jeanne", "Re: FW: Anna's Salary yes", "FW: FW: s Salary Jeffrey EFTA00832952"]	["EFTA02509047", "EFTA00717912", "EFTA00855850", "EFTA00845271", "EFTA00832951", "EFTA00852851", "EFTA00689796", "EFTA00838226", "EFTA00839735", "EFTA00842046"]
682	Jeffrey Epstein	Nicole Junkermann	49	0201-11-02	2014-28-04	45	4	["Re: first On Fri, Feb 17, 2017 at 9:51 PM, Nicole Junkermann", "I have gates on wed, if you would like to join for part.. also why dont you consider working for/with me , organizing the worlds most intersintng poepl, you can invest alongsie, you can re structure h", "Re: I know them well. is it for you'll On Mon, Apr 28, 2014 at 6:01 AM, Nicole Junkermann > wrote: What do u think about fake breast?", "Re: I know them well. is it for you'll On Mon, Apr 28, 2014 at 6:01 AM, Nicole Junkermann < wrote: What do u think about fake breast?", "Re: I know them well. is it for you?\\\\ On Mon, Apr 28, 2014 at 6:01 AM, Nicole Junkermann < > wrote: What do u think about fake breast?"]	["EFTA01764889", "EFTA01751680", "EFTA00721086", "EFTA00992670", "EFTA00663174", "EFTA00663525", "EFTA00639667", "EFTA00637816", "EFTA01763214", "EFTA00992663"]
683	Caroline Lang	Jeffrey Epstein	61	\N	\N	2	59	["Im in paris all week, hope to see you and family please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and ", "where should we meet.? how was yesterday? look forward to it The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and ", "any progress? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for EFTA00655499", "sorry but we should delay dsk until i know my schedule unlikely to come before the 15th please note The information contained in this communication is confidential, may be attorney-client privileged, ", "any progress? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. "]	["EFTA00672166", "EFTA00932235", "EFTA00702337", "EFTA00932005", "EFTA00662620", "EFTA00652457", "EFTA00817056", "EFTA00672162", "EFTA00817164", "EFTA00932028"]
684	Barry Josephson	Jeffrey Epstein	26	\N	\N	1	25	["<no subject> weather must be a killer today please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is in", "Re: Why not Amazon or apple On Saturday, August 29, 2015, Barry Josephson wrote:", "I will be in miami on fri at 5\\u201e where will you guys be The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is int", "<no subject> diiiner with woody thurs? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intende", "Re: Why not Amazon or apple On Saturday, August 29, 2015, Barry Josephson < wrote:"]	["EFTA00847429", "EFTA01744801", "EFTA01193310", "EFTA01847346", "EFTA00639998", "EFTA00847425", "EFTA01197355", "EFTA01193307", "EFTA02016347", "EFTA00849004"]
685	Jeffrey Epstein	Mark Lloyd	29	\N	\N	25	4	["Re: im in paris\\u201e where are you and what are you doing? On Tue, Mar 8, 2011 at 12:27 AM, Mark Lloyd 4:: > wrote: Jefrey, Just got back to London and read the headlines. Not sure there is anything I can", "Re: Payment", "Re: tomoroow aftemnon On Wed, Sep 29, 2010 at 12:35 AM, Mark Lloyd \\u2022:: > wrote: Brilliant news!! Yes. When do I see you???? Sent from my iPhone On 29 Sep 2010, at 00:33, Jeffrey Epstein <jeevacationOg", "Re: tornoroow aftemnon mail.com> On Wed, Sep 29, 2010 at 12:35 AM, Mark Lloyd e > wrote: Brilliant news!! Yes. When do I see you???? Sent from my iPhone On 29 Sep 2010, at 00:33, Jeffrey Epstein leeva", "Re: im in paris\\u201e where are you and what are you doing? On Tue, Mar 8, 2011 at 12:27 AM, Mark Lloyd <-> wrote: Jefrey, Just got back to London and read the headlines. Not sure there is anything I can d"]	["EFTA00697243", "EFTA01861798", "EFTA00755030", "EFTA01047634", "EFTA00897502", "EFTA01883056", "EFTA01892338", "EFTA00914365", "EFTA02016291", "EFTA00914348"]
686	Greg Wyler	Jeffrey Epstein	34	\N	\N	1	33	["997 please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee", "thanks for all your help. how is your project progressing lik************************************************** ******* The information contained in this communication is confidential, may be attaney-", "Re: I don't have a side . I can easily buy it. you will need to structure your side. - either way .- little value given by anyone to spectrum in an outright purchase without it being operational. .and", "thanks for all your help. how is your project progressing \\u2022\\u2022******\\u2022\\u2022***** ***** *** ***** *** ****** ** ***** ** ***** *** *** The information contained in this communication is confidential, may be a", "thanks for all your help. how is your project progressing Am********************************************************* The information contained in this communication is confidential, may be attomey-di"]	["EFTA00991493", "EFTA00964533", "EFTA00970152", "EFTA00964536", "EFTA01790825", "EFTA00991499", "EFTA00991496", "EFTA00695241", "EFTA01135033", "EFTA01920522"]
687	Lawrence Krauss	Richard Kahn	7	2015-02-11	2015-04-12	7	0	["a slight amendment of the gift letter, if possible. Dear Rich: I hope he New Year is going well. Thanks for coordinating the gift to Origins so quickly in Dec. I just found out", "a slight amendment of the gift letter, if possible. Dear Rich: I hope he New Year is going well. Thanks for coordinating the gift to Origins so quickly in Dec. I just found out", "a slight amendment of the gift letter, if possible. Dear Rich: EFTA00679787", "Re: Cynthia", "Re: > >, Cynthia \\u2039 >"]	["EFTA00667781", "EFTA01933413", "EFTA01933286", "EFTA01931431", "EFTA00711270", "EFTA00642828", "EFTA00679786"]
688	Jeffrey Epstein	Stuart Hameroff	2	\N	\N	2	0	["did it get resolved. . what is your side please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is inten", "Re: who are the speakers and what is the cost. lm in for at least 50k, before knowing anyhing On Thu, Mar 30, 2017 at 11:17 PM, Hameroff, Stuart R - (hameroff)"]	["EFTA00697075", "EFTA00643937"]
689	Andrew Farkas	Jeffrey Epstein	94	\N	\N	17	77	["Re: A Hint", "You and i enjoy a special relationship that i cherish, and we both appreciate full disclosure, for good or bad, I", "Re:", "Re: Any news from your end? yes as promised however shabaz said you only woud let them in for up to 300 , as you told them you had many other interested, so they will confirm up to 200. m ? im going t", "Re: can you call mr On Sat, Oct 3, 2015 at 4:48 PM, Farkas, Andrew L. < > wrote: Tomorrow lunch?"]	["EFTA00836663", "EFTA00836671", "EFTA00680228", "EFTA00715210", "EFTA00714108", "EFTA00707556", "EFTA00855247", "EFTA00716745", "EFTA00836653", "EFTA00836658"]
731	Alan Dershowitz	Harry Beller	3	\N	\N	3	0	["Please send me your numbers in preparation for my call with jeffrey.please include total fee paid to me, which you said was 30k plus more than my figure. Also total hours you say I billed(which you sa", "Re:", "Please send me your numbers in preparation for my call with jeffrey.please include total fee paid to me, which you said was 30k plus more than my figure. Also total hours you say I billed(which you sa"]	["EFTA00770482", "EFTA00884571", "EFTA00740185"]
690	Jeffrey Epstein	Michael Ovitz	10	\N	\N	10	0	["want to come to dinner tomorrow , intersting people.or sat lunch\\u201e you call bring her if you want The information contained in this communication is confidential, may be attorney-client privileged, may", "want to come to dinner tomorrow , intersting people.or sat lunch\\u201e you can bring her ,if you want The information contained in this communication is confidential, may be attorney-client privileged, may", "want to come to dinner tomorrow , intersting people.or sat lunch\\u201e you can bring her ,if you want The information contained in this communication is confidential, may be attorney-client privileged, may", "want to come to dinner tomorrow , intersting people.or sat lunch\\u201e you can bring her ,if you want The information contained in this communication is confidential, may be attorney-client privileged, may", "want to come to dinner tomorrow , intersting people.or sat lunch\\u201e you can bring her ,if you want The information contained in this communication is confidential, may be attorney-client privileged, may"]	["EFTA01769486", "EFTA01873254", "EFTA00877416", "EFTA01769872", "EFTA00647873", "EFTA00647879", "EFTA01987295", "EFTA00660245", "EFTA01767594", "EFTA01873089"]
691	Brice Gordon	Richard Kahn	25	2014-09-19	2018-07-31	20	5	["ZDC-HWS Leak/Cut Area", "LSJ: Lady K Emad", "Fwd: ZDC EGP Wall Height", "Re: LSJ Main Distribution Pumps", "ZDC-HWS Leak/Cut Area"]	["EFTA01048190", "EFTA01016179", "EFTA01877497", "EFTA01902720", "EFTA02061055", "EFTA01782700", "EFTA01798811", "EFTA01005506", "EFTA01904411", "EFTA01202015"]
692	Brice Gordon	Gary Kerney	4	\N	\N	4	0	["Re: is this accurate Sony for the late response have got back into cell area The answer is No And who reported this? Sent from my iPhone On Dec 15, 2010, at 8:29 AM, \\"Jeffrey Epstein\\" leevacation@gmai", "FW: Zorro Fountain Install Hi there Yes all info was forward to JEE, even the note from you agreeing with my approach", "LSJ: Lady K Emad", "FW: Zorro Fountain Install 1-ii there Yes all info was forward to JEE, even the note from you agreeing with my approach"]	["EFTA00649066", "EFTA02721277", "EFTA00744080", "EFTA00750567"]
693	Anthony Barrett	Jeffrey Epstein	3	2013-10-29	2013-12-04	0	3	["Re: let me think about it, it seems more prone to operational diffictulties than real estate On Tue, Oct 29, 2013 at 10:54 AM, Anthony Barrett wrote: Jeffrey,", "Re: let me think about it, it seems more prone to operational diltictultics than real estate On Tue, Oct 29, 2013 at 10:54 AM, Anthony Barrett < > wrote: Jeffrey,"]	["EFTA01140567", "EFTA00651563", "EFTA01756668"]
694	Jay Lefkowitz	Steven Sinofsky	2	\N	\N	1	1	["Re:", "Re: privileged I understand the practical nature of this. I am a bit concerned about my future employability in a competitive environment in this regard and the PR implications of people writing that "]	["EFTA00652526", "EFTA00962143"]
695	Jeffrey Epstein	Steven Sinofsky	24	2012-11-14	2012-11-14	22	2	["news , what are you up to? im leading jay,now need a kick in the ass ************rrrrrrr*******\\u2022\\u2022w*******************rrr*******\\u2022 The information contained in this communication is confidential, may be", "contract", "lots of chatter . stay focused on what you want and how to mazimize its liklihood * The information contained in this communication is confidential, may be attorney-client privileged, may constitute i", "Re: ill ask after the first of year . i see little downside in you visiting china, alibaba doing its own os. how did the dinner with adreeson go? On Sun, Dec 30, 2012 at 11:51 AM, Steven Sinofsky wrot", "Re: ill ask after the first of year . i see little downside in you visiting china, alibaba doing its own os. how did the dinner with adreeson go? On Sun, Dec 30, 2012 at 11:51 AM, Steven Sinofsky wrot"]	["EFTA01762851", "EFTA00962148", "EFTA00951708", "EFTA00951712", "EFTA00951698", "EFTA00951692", "EFTA01900363", "EFTA01910637", "EFTA00701382", "EFTA00874938"]
696	Ehud Barak	Jeffrey Epstein	9	\N	\N	0	9	["Boris, I m happy to come to zurich on thurs . However as Ariane filled me in on your meeting. Do you think my coming ,at least for the moment, is useful. ? please note The information contained in thi", "Boris, I m happy to come to zurich on thurs . However as Ariane filled me in on your meeting. Do you think my coming ,at least for the moment, is useful. ? please note The information contained in thi", "Boris, Tuesday I have a full day meeting with AR. do you have any time on wed or thurs ? please note The information contained in this communication is confidential, may be attorney-client privileged,", "Boris, Tuesday I have a full day meeting with AR. do you have any time on wed or thurs ? please note The information contained in this communication is confidential, may be attorney-client privileged,", "Boris, Tuesday I have a full day meeting with AR. do you have any time on wed or thurs ? please note The information contained in this communication is confidential, may be attorney-client privileged,"]	["EFTA02365520", "EFTA02365451", "EFTA02659283", "EFTA00662368", "EFTA02366328", "EFTA00654506", "EFTA02662047", "EFTA02659447", "EFTA00662410"]
697	Mark Lloyd	Richard Kahn	12	2012-07-18	2012-07-18	0	12	["Re: promissory note attached are bank details for incoming wire bank name: jp morgan chase rt #:021000021 account # account name: jeffrey epstein please let me know when you plan to send funds so i ca", "Re: promissory note great thank you PLEASE NOTE EFFECTIVE JUNE 5TH MY CONTACT INFO WILL BE AS FOLLOWS: Richard Kahn tel fax cell On Jun 1, 2012, at 11:25 AM, Mark Lloyd wrote:", "Re: promissory note great thank you PLEASE NOTE EFFECTIVE JUNE 5TH MY CONTACT INFO WILL BE AS FOLLOWS: Richard Kahn tel fax cel On Jun 1, 2012, at 11:25 AM, Mark Lloyd wrote: EFTA00692825", "Re: promissory note great thank you PLEASE NOTE EFFECTIVE JUNE 5TH MY CONTACT INFO WILL BE AS FOLLOWS: Richard Kahn fel= fax cel On Jun 1, 2012, at 11:25 AM, Mark Lloyd wrote:", "Re: promissory note just a reminder that the promissory note is due July 31st the balance due on july 31st with accrued interest is 162,674 please let me know if you need wiring instructions thank you"]	["EFTA01888603", "EFTA00941629", "EFTA01876996", "EFTA00940154", "EFTA02360191", "EFTA01875187", "EFTA00659361", "EFTA00657164", "EFTA00692824", "EFTA02004887"]
698	Austin Hill	Jeffrey Epstein	24	\N	\N	0	24	["Re: ready On Sat, Sep 16, 2017 at 12:56 PM, jeffrey E. <jeevacation@gmail.com> wrote:", "now? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addresse", "austin, . best laid plans. unfortunately I came down with a bad cold. we should postpone. . we can try to skype either on sat or sun. but not sure of my level of attention yet. sorry please note The i", "Re: Time to chat 7 -8 paris? or weekend easy ill be in new york , if you and some guys want to visit at my expense On Tue, Oct 17, 2017 at 3:19 PM, Austin Hill < wrote:", "Re: Time to chat 7 -8 paris? or weekend easy ill be in new york , if you and some guys want to visit at my expense On Tue, Oct 17, 2017 at 3:19 PM, Austin Hill < > wrote:"]	["EFTA00665479", "EFTA02608800", "EFTA02608843", "EFTA02371541", "EFTA02396170", "EFTA02362030", "EFTA02606001", "EFTA00982818", "EFTA01004644", "EFTA00658061"]
699	Daniel Siad	Jeffrey Epstein	5	\N	\N	1	4	["Re:"]	["EFTA01981567", "EFTA00701151", "EFTA01777553", "EFTA00701411", "EFTA00659358"]
700	Jeffrey Epstein	Larry Summers	9	2014-03-08	2014-03-08	9	0	["today? call? *********************************************************** The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside infor", "Re: i am glad to hear that you can do at least one thing without guilt On Sat, Feb 2, 2019 at 6:51 PM Larry Summers wrote: Always amusing. And I can now without guilt make massage jokes! Sent from my ", "Re: Re:", "today? call? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee. I", "Re: Sony the dates were wrong 19th as per Julie On Saturday, March 8, 2014 Larry Summers wrote:"]	["EFTA01029002", "EFTA02538032", "EFTA01933510", "EFTA02627678", "EFTA01779382", "EFTA01933437", "EFTA02030468", "EFTA01028863", "EFTA00661389"]
701	Cecile de Jongh	Emad Hanna	1	\N	\N	1	0	["Re: Fuel Truck Also, I will wait for more info from Emad on the truck before I send the specs to"]	["EFTA00666471"]
702	Jeffrey Epstein	Jennie Saunders	33	\N	\N	31	2	["no problem , talk to me bout michele for the develpoent job The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and i", "send photos\\u201eyou are goin to have a great time DISCLAIMER Important! This message is intended for the above named person(s) only and is", "send photos\\u201eyou are goin to have a great time DISCLAIMER Important! This message is intended for the above named person(s) only and is", "Re: You can try but I doubt it Sent from my iPhone On Mar 5, 2010, at 8:08 AM, \\"Jennie Saunders\\" < wrote: U available ? D apt question ... Is it better to sell at 450 or try to give back property back", "Re: what is his name?"]	["EFTA00882391", "EFTA00671109", "EFTA00776602", "EFTA00879084", "EFTA00749612", "EFTA00774517", "EFTA00666544", "EFTA00899545", "EFTA00882428", "EFTA01780462"]
703	Arda Beskardes	Jeffrey Epstein	3	\N	\N	3	0	["Re: should i", "Re: should i", "Re:"]	["EFTA00666923", "EFTA01038175", "EFTA00995524"]
704	Alan Dershowitz	Jeffrey Epstein	8	2015-01-08	2015-01-08	5	3	["Re: 2015 0107 The Independent_Prince Andrew.pdf", "Re: Intervention/ bill for legal services", "Re: my edits An attorney for Jeffrey Epstein today issued the following statement: Despite inaccurate reports to the contrary, the government did not charge, nor were there ever allegations that Jeffr", "Re: my edits", "Re: I'm in NY Unfortunately no. Off to LA on Friday. What's new? Sent from my iPhone On May I, 2012, at 9:08 AM, Jeffrey Epstein <jeevacation@gmail.com> wrote: saturday\\u201e will you still be there On Tue"]	["EFTA01200191", "EFTA00673195", "EFTA00905860", "EFTA01200199", "EFTA00884660", "EFTA00905884", "EFTA00866565", "EFTA00740317"]
705	George Church	Jeffrey Epstein	8	\N	\N	2	6	["Following up on our conversation in LA > Thanks for the introduction. I believe that you both were interested in our disruptive technologies (precise, fast and inexpensive) for human genome (and micro", "Following up on our conversation in LA Thanks for the introduction. I believe that you both were interested in our disruptive technologies (precise, fast and inexpensive) for human genome (and microbi", "Re: value I have a great idea. lets speak today if possible please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside inform", "Re: value I have a great idea. lets speak today if possible please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside inform", "Re: value I have a great idea. lets speak today if possible please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside inform"]	["EFTA01916477", "EFTA00677967", "EFTA01980272", "EFTA01920172", "EFTA00874023", "EFTA01919154", "EFTA01980600", "EFTA01917108"]
706	Jeffrey Epstein	Mark Tramo	14	\N	\N	13	1	["Fwd: The Institute for Music and Brain Science, Inc. - Materials Completed, Shipped"]	["EFTA00777658", "EFTA00752378", "EFTA00752371", "EFTA01981850", "EFTA00679322", "EFTA02416806", "EFTA01982409", "EFTA01981991", "EFTA01981924", "EFTA02416709"]
707	Jeffrey Epstein	Mark Epstein	13	\N	\N	13	0	["Re: hey im in carib. who are the childrens guardians? did you leave them money in trust. trustees? joyce? if you left them property, estate tax and admin? who decides? maybe consider dividing assets n", "Fwd: Marks wife/girlfriend", "Are your tryglerides high please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for th", "Re:", "Re:"]	["EFTA00995295", "EFTA02533210", "EFTA01057392", "EFTA02665617", "EFTA01057384", "EFTA01915067", "EFTA00681247", "EFTA02533372", "EFTA01968377", "EFTA01916373"]
708	Anthony Barrett	Lesley Groff	3	\N	\N	3	0	["Meetings with Jeffrey >, Francis Barany Just wanted to thank you for arranging the meetings on Saturday. I have attached additional info on the two projects that Francis presented to JE and Henry. You", "Meetings with Jeffrey Lesley, , Francis Barany Just wanted to thank you for arranging the meetings on Saturday. I have attached additional info on the two projects that Francis presented to JE and Hen", "Meetings with Jeffrey Lesley, , Francis Barany Just wanted to thank you for arranging the meetings on Saturday. I have attached additional info on the two projects that Francis presented to JE and Hen"]	["EFTA01741026", "EFTA00687529", "EFTA01741006"]
709	Paul Morris	Richard Kahn	34	2014-05-30	2014-10-20	3	31	["wires can you please update me on status of 2 wires hitting Southern Trust account 9244 thank you Richard Kahn", "Re: Citi Preferred [C] please work $3,000,000 order at 100.00 for Citi Preferred Q please email or call Darren if you need to confirm thank you Richard Kahn", "Re: Noam", "Re: Noam", "Re: Dispersion Call Option [C] please confirm bid of 0.60% converted to dollars is 24,996 thank you Richard Kahn"]	["EFTA00862678", "EFTA01412968", "EFTA00862651", "EFTA01421823", "EFTA01468922", "EFTA01399962", "EFTA01474183", "EFTA01470457", "EFTA01471339", "EFTA01470449"]
710	Martin Weinberg	Richard Kahn	7	\N	\N	2	5	["RE: Confidential Thank you Rich Kahn", "RE: Confidential Receipt confirmed, thanks Marty", "RE: Confidential 'thank you Rich Kahn", "CONFIDENTIAL - JE Rich"]	["EFTA00899441", "EFTA00774591", "EFTA00712152", "EFTA00881565", "EFTA00941006", "EFTA00692837", "EFTA00775362"]
711	Al Seckel	Jeffrey Epstein	93	\N	\N	3	90	["Re: of course On Thu, Apr 16, 2009 at 5:55 PM, AI seckel alla wrote: Ah, you have actually asked my speciality. Seriously. Ok, different disciplines and business too?", "Re: of course On Thu, Apr 16, 2009 at 5:55 PM, AI seckel alla wrote: Ah, you have actually asked my speciality. Seriously. Ok, different disciplines and business too?", "Re: of course On Thu, Apr 16, 2009 at 5:55 PM, AI seckel alla wrote: Ah, you have actually asked my speciality. Seriously. Ok, different disciplines and business too?", "Re: MIKE IS STILL ON CALL, HE HAS BEEN WAITING 45 MINUTES FOR YOU. there was no time agreed.. just send me his phone number asap On Wed, Dec 8, 2010 at 1:07 PM, Al seckel <", "Re: hey"]	["EFTA00710795", "EFTA00752907", "EFTA00750539", "EFTA00752719", "EFTA00749108", "EFTA00751380", "EFTA00740161", "EFTA00752919", "EFTA00740153", "EFTA00753308"]
712	Emad Hanna	Gary Kerney	27	2010-09-29	2011-09-12	15	12	["L.S3 Check All, contact; ; LSJ JE asked me to negotiate the invoiced amount of $ 4,860 and I got the vendor down to $ 4,080 and we agreed to use him exclusively when renting machine for a period of 1 ", "flagpole Sorry here's the flagpole budget EFTA00705435", "RE: Dear Robert and Richard We will be winding down construction over the next several weeks. As you get your program together please do not hesitate to contact us, and if possible visit Little St.Jam", "Tara Faucets", "RE: tiki budget Gary,"]	["EFTA01795489", "EFTA00900147", "EFTA00900630", "EFTA00905154", "EFTA00900707", "EFTA00705434", "EFTA00696648", "EFTA01774292", "EFTA01795532", "EFTA00905164"]
713	Emad Hanna	Richard Kahn	10	2011-02-24	2011-02-24	10	0	["L.S3 Check All, contact; ; LSJ JE asked me to negotiate the invoiced amount of $ 4,860 and I got the vendor down to $ 4,080 and we agreed to use him exclusively when renting machine for a period of 1 ", "LS) Wire Rich,", "Urgent LSJ Wire Rich, Please wire $ 12,000 for the attached Thank you Emad Hanna Project Controller HBRK Associates 301 East 66th St Suite 10F New York, NY 10065 The information contained in this comm", "Urgent LSJ Wire Rich, Please wire S 12,000 for the attached Thank you Emad Hanna Project Controller HBRK Associates 301 East 66th St Suite 10F New York, NY 10065 ######################################", "LSJ New Pool EFTA00906202"]	["EFTA00906201", "EFTA00900707", "EFTA02023080", "EFTA01836426", "EFTA00696648", "EFTA00900630", "EFTA00761558", "EFTA02012574", "EFTA01779823", "EFTA01858779"]
714	Daphne Wallace	Emad Hanna	6	2011-02-24	2011-02-24	0	6	["L.S3 Check All, contact; ; LSJ JE asked me to negotiate the invoiced amount of $ 4,860 and I got the vendor down to $ 4,080 and we agreed to use him exclusively when renting machine for a period of 1 ", "Urgent LSJ Wire Rich, Please wire $ 12,000 for the attached Thank you Emad Hanna Project Controller HBRK Associates 301 East 66th St Suite 10F New York, NY 10065 The information contained in this comm", "Urgent LSJ Wire Rich, Please wire S 12,000 for the attached Thank you Emad Hanna Project Controller HBRK Associates 301 East 66th St Suite 10F New York, NY 10065 ######################################", "Urgent LSJ Wire Rich, Please wire $ 12,000 for the attached Thank you Emad Hanna Project Controller HBRK Associates 2 EFTA_R1_00097981 EFTA01779824", "L.S3 Check All, EFTA_R1_00217277 EFTA01836427"]	["EFTA00900707", "EFTA01836426", "EFTA00696648", "EFTA00900630", "EFTA02012574", "EFTA01779823"]
715	Brad Karp	Jeffrey Epstein	90	\N	\N	0	90	["Re: i will ask, of course. can you tell me what role he would like to fill i know little about the movies On Wed, Jun 1, 2016 at 5:18 PM, Karp, Brad S Jeffrey, Can I raise a personal issue with you co", "Re: tomo-thurs On Mon, Jul 10, 2017 at 11:09 PM, Karp, Brad S wrote:", "please note > > The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addressee", "Re: we agree , a baseless claim can include whatever they like. including the cancer text , plus allegatations of xyz and more On Sun, Jul 26, 2015 at 9:47 AM, Karp, Brad S < <mailto wrote: I think th", "when i return I think we really must insist on a sit down<=r clear=\\"all\\"> please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute"]	["EFTA02391100", "EFTA02347549", "EFTA02377471", "EFTA02215334", "EFTA02372647", "EFTA02405705", "EFTA02447245", "EFTA02341191", "EFTA02343580", "EFTA02391272"]
716	Bobby Kotick	Jeffrey Epstein	6	\N	\N	0	6	["the girls and i are going to see elon musk at space x tomorrow, are you around, *********************************************************** The information contained in this communication is confident", "the girls and i are going to see elon musk at space x tomorrow, are you around, *********************************************************** The information contained in this communication is confident", "the girls and i are going to see elon musk at space x tomorrow, are you around, The information contained in this communication is confidential, may be attorney-client privileged, may constitute insid", "the girls and i arc going to see don musk at space x tomorrow, arc you around, The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside", "the girls and i are going to see don musk at space x tomorrow, are you around, The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside"]	["EFTA00954885", "EFTA00700778", "EFTA01762793", "EFTA01973391", "EFTA01902917", "EFTA01902855"]
717	Jeffrey Epstein	Leon Black	19	\N	\N	19	0	["Bann J. Cohen WE are DONE !!", "Consistent with the message I just left on your phone cld we use the following language on p.2 of the 1040x's: \\"This return is being filed solely to provide information pursuant to the Voluntary Progr", "schedule of real estate taxes. .. ? page 675 commiosn and fees? 2 m and no 1099s/ ? arizona house matched sales and cost? no commsions? please note The information contained in this communication is c", "Re: [External] again, please give me names and not titles. i have no idea who you spoke to,? the fun thing is that you will not get an answer . same for tax issues. they only respond and do of initiat", "Re: We were told that neither Deloitte or apollo tax knew of this . That was the first question On Sun, Apr 30, 2017 at 6:18 PM Thomas Turrin < > wrote:"]	["EFTA02400622", "EFTA02651318", "EFTA01054188", "EFTA01047854", "EFTA02448211", "EFTA00711457", "EFTA02651711", "EFTA02659677", "EFTA01054186", "EFTA01002946"]
718	Andrew Farkas	Brock Pierce	3	\N	\N	0	3	["Re: Jeffrey,", "Re:", "Re: 2 EFTA_R1_01428850 EFTA02396514"]	["EFTA01922064", "EFTA02396513", "EFTA00707011"]
719	Brock Pierce	Jeffrey Epstein	11	\N	\N	3	8	["Re: Jeffrey,", "Re: Re: great email tomorrw On Fri, Jan 21, 2011 at 5:40 AM, Brock Pierce wrote: Beijing through the weekend. I won't be busy so I am available to talk whenever is convenient for you. Let me know what", "Re: Re: great email tomorrw On Fri, Jan 21, 2011 at 5:40 AM, Brock Pierce > wrote: Beijing through the weekend. I won't be busy so I am available to talk whenever is convenient for you. Let me know", "Re: Re: Next week or march 6-7 Sony for all the typos .Sent from my iPhone On Feb 18, 2011, at 3:51 PM, Brock Pierce < > wrote: I'm scheduling a trip to NY in the next few weeks. Let me know when you'", "Re: Re: =/div> great email tomorrw 21, 2011 at 5:40 AM, Brock Pierce > wrote: 2 EFTA_R1_00129698 EFTA01794906"]	["EFTA01922064", "EFTA00904276", "EFTA00905741", "EFTA00904273", "EFTA02396513", "EFTA01794894", "EFTA02017800", "EFTA02722540", "EFTA02721760", "EFTA01794905"]
720	Bill Gates	Steven Sinofsky	1	\N	\N	0	1	["Re: Trip Report: Bioscience & Philanthropy Summit (Allen Institute) I think this is a new event and as with all new events it takes a couple of iterations to arrive at complete clarity. They have been"]	["EFTA00707678"]
732	Doug Schoettle	Richard Kahn	4	\N	\N	4	0	["Re: EFTA00749370", "Re: Dear Jeffrey, I have not been getting any e-mails form you or Rich Khan except one from Rich on may 18. I have been", "Re: Dear Jeffrey, I have not been getting any e-mails form you or Rich Khan except one from Rich on may 18. I", "Re: Dear Jeffrey, I have not been getting any e-mails form you or Rich Khan except one from Rich on may 18. I"]	["EFTA00892201", "EFTA02413634", "EFTA02414027", "EFTA00749369"]
721	Al Seckel	Cecile de Jongh	3	\N	\N	3	0	["Re: MINDSHIFT That would be perfect!!!! :-) Isabel and I have arc part of the Academy Award screeners, which means we get all the movies in advance, including before they hit the theaters, and so, we ", "Re: MINDSHIFT Talks each and lunch on sat On the island Sorry for all the typos .Sent from my iPhone On Dec 17, 2010, at 3:48 PM, Cecile de Jongh wrote: Is there anything I can do to help get this mov", "Re: MINDSHIFT That would be perfect!!!! :-) Isabel and I have are part of the Academy Award screeners, which means we get all the movies in advance, including before they hit the theaters, and so, we "]	["EFTA02001049", "EFTA01831952", "EFTA00709083"]
722	Deepak Chopra	Richard Kahn	2	2017-10-18	2017-10-18	0	2	["Fwd: Thank you !", "Fwd: Thank you !"]	["EFTA02401235", "EFTA00711477"]
723	Jeffrey Epstein	Peter Mandelson	89	\N	\N	88	1	["Re: still there? On Mon, Jul 16, 2012 at 4:59 AM, Peter Mandelson > wrote: I know as much (little) as anyone else. Who others at Barclays do you mean, left or still there ?", "I will be in paris starting tomorrow \\u2022********************************************************** The information contained in this communication is confidential, may be attorney-client privileged, may", "I never mention you to Landon.. keep it that way", "Hugo Swine , did you have a run in? *********************************************************** The information contained in this communication is confidential, may be attorney-client privileged, may ", "Hugo Swire , did you have a run in? *********************************************************** The information contained in this communication is confidential, may be attorney-client privileged, may "]	["EFTA00766945", "EFTA00756864", "EFTA00894142", "EFTA00712288", "EFTA00756858", "EFTA00751789", "EFTA00756436", "EFTA00897309", "EFTA00769306", "EFTA00742741"]
724	Jay Lefkowitz	Richard Kahn	2	\N	\N	2	0	["Re: Jeffrey Epstein invoices Rich, I went back over the bills with my billing agent. I was getting confused by the various write offs we have done", "Re: Jeffrey Epstein invoices Rich, I went back over the bills with my billing agent. I was getting confused by the various write offs we have done"]	["EFTA00718562", "EFTA00876016"]
725	Glenn Dubin	Jeffrey Epstein	4	\N	\N	0	4	["still no agreement. , briger, corbin The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the", "still no agreement. , briger, corbin The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the", "Did you and Zwim settle. ? I assume that is a good thing *********************************************************** The information contained in this communication is confidential, may be attorney-cl", "Fwd: > >"]	["EFTA00922432", "EFTA02535993", "EFTA02408668", "EFTA00720037"]
726	Boris Nikolic	Nicole Junkermann	3	2014-27-06	2014-27-06	1	2	["RE: Thank you lee!", "Fwd: CV WEF Boris, Just in case you did not find my cv Best Nicole Sent fmm ftry Samsung Gassy utarepbone", "Fwd: CV WEF Boris, Just in case you did not find my cv Best Nicole Sent fmm ftry Samsung Gassy utarepbone"]	["EFTA01916625", "EFTA00720993", "EFTA01915599"]
727	Doug Schoettle	Jeffrey Epstein	14	\N	\N	4	10	["Re: LS) Update I would like to see arch kitchen windows. , less long straight stair cases. more romantic. roof for screening roon, On Thu, Aug 5, 2010 at 8:25 PM, Ken-Hao Hsu Team,", "Re: have they gone out to bid as we decided last tuesday? On Mon, Sep 27, 2010 at 4:30 PM, Matthew Milne Doug,", "i just found out that no one has appover the various white fans\\u201e doug thought the electirican ordered, gary does n't know who approved.. emad didn't ask my approval or anyone else for that matter. i h", "Re: Fw: LSJ_SCHEME DI D2 & D3_20100712 Warwick, as i said in our call last night\\u201e you are not using the topos that you have.. these drawings are so inaccurate , as to render them useless. There is onl", "Re: EFTA00749370"]	["EFTA02527834", "EFTA00733714", "EFTA00736661", "EFTA02434432", "EFTA02414027", "EFTA00749369", "EFTA00731715", "EFTA00754702", "EFTA00892201", "EFTA02413634"]
728	Doug Schoettle	Gary Kerney	5	\N	\N	0	5	["RE: LSJ Update Warwick These look good,we'll understand all the stairs in the screen complex better when we see the 3D renderings, as well the scale of the", "RE: LSJ Update Warwick These look good,we'll understand all the stairs in the screen complex better when we see the 3D renderings, as well the scale of", "RE: LSJ living room and screening room Warwick After spending the week on island Jeffrey believes his idea is sound.he will make the existing livingroom as good as a", "RE: LSJ living room and screening room Warwick After spending the week on island Jeffrey believes his idea is sound.he will make the existing livingroom as good as a theater room it", "RE: Plan Study G-2 Warwick One comment I have is Jeffrey does not want to come up the stairs from the master bedroom and be"]	["EFTA00736014", "EFTA00737561", "EFTA00779398", "EFTA00758326", "EFTA02413952"]
729	Dr. Jarecki	Jeffrey Epstein	13	\N	\N	0	13	["henry \\u201e do you need", "you didnt tell me how much you were in for re the Harvard Evolution Program.. 500- l m, we can handle 3m ########################################################### The information contained in this c", "EFTA00764774", "has anyone looked at if your scholars :work : has been cited after rescue, and how it compares with before ? The information contained in this communication is confidential, may be attorney-client pri", "you didnt tell me how much you were in for re the Harvard Evolution Program.. 500- l m, we can handle 3m ########################################################### The information contained in this c"]	["EFTA00900136", "EFTA01826592", "EFTA00891187", "EFTA00764773", "EFTA01831406", "EFTA02426748", "EFTA00764776", "EFTA01797840", "EFTA01800379", "EFTA01831936"]
730	Jeffrey Epstein	Stephen Kosslyn	11	\N	\N	11	0	["Re: Dates for a visit? TCS? any time is good for me, i would like to wait until the first week in sept to confirm\\u201e so that my schedule isfree On Wed, Aug 19, 2009 at 12:20 PM, Stephen Kosslyn wrote:", "Re: \\"Duplexity\\" v3 cheat sheet : committes are a way of life.. business, charity, arts, govt.. they. from roman times up until the discovery of the scientific K-E , Method Of ( KEMO) committee composi", "Re: <no subject> thanks\\u201e hope things are well... can robin give me a namne of a child pyshologist in new yokr ocd behavior, young girl", "Re: \\"Duplexity\\" v3 cheat sheet : committes are a way of life.. business, charity, arts\\u201e govt.. they. from roman times up until the discovery of the scientific K-E , Method Of ( KEMO) committee composi", "Re: \\"Duplexity\\" v3 I believe I have a great idea . I think you can use this in a way that would make money, get you involved with interesting people, have you work on your traslational cognitive stuff"]	["EFTA00739819", "EFTA00773824", "EFTA00765214", "EFTA00740824", "EFTA00771571", "EFTA00771566", "EFTA00772490", "EFTA00773829", "EFTA00884915", "EFTA02441332"]
733	Jeffrey Epstein	Katie Couric	2	\N	\N	2	0	[]	["EFTA00751207", "EFTA00751204"]
734	Al Seckel	Stephen Kosslyn	1	\N	\N	0	1	["Re: Clearing some matters"]	["EFTA00751373"]
793	Boris Nikolic	Ehud Barak	2	\N	\N	0	2	["Fwd: Parasight Ltd. Dear Boris", "Re: Parasight Ltd. Boris"]	["EFTA01961765", "EFTA01961245"]
736	David Stern	Jeffrey Epstein	11	\N	\N	4	7	["david, I want to take pictures of a house for sale on belgrave square, please contact Mrs Wasserstein and photograph for me. you can take the duchess **************************************************", "Re: Larry,", "Fwd: China", "I need to organize that Karima Nigmatulina who is in charge of city planning of Moscow (she reports to Mayor of Moscow) meets someone (anyone \\u2014 can be junior) in the office of London Mayor who is doin", "david, I want to take pictures of a house for sale on bclgrave square, please contact Mrs Wasserstein and photograph for me. you can take the duchess ***** ************* * ********* ******************"]	["EFTA00861584", "EFTA02428903", "EFTA00935684", "EFTA02512117", "EFTA00762672", "EFTA00990305", "EFTA02438800", "EFTA01765775", "EFTA01825070", "EFTA02025265"]
737	Jeffrey Epstein	Kenneth Starr	2	\N	\N	1	1	["Re:"]	["EFTA00763983", "EFTA02633022"]
738	Jeffrey Epstein	Roy Black	3	\N	\N	3	0	["hire bill ritchie to handle your subpoena\\u201e asap It will be made clear that you are working for critten and not roy The information contained in this communication is confidential, may be attorney-clie", "hire bill ritchie to handle your subpoena\\u201e asap It will be made clear that you are working for critten and not roy The information contained in this communication is confidential, may be attorney-clie"]	["EFTA02436957", "EFTA00770194", "EFTA00965704"]
739	Eva Dubin	Peggy Siegal	1	\N	\N	1	0	["RE:"]	["EFTA00770921"]
740	Jes Staley	Mary Erdoes	2	\N	\N	1	1	["Re: Deutsche Bank confirms talks on strategic partnership with Sal. Oppenheim Group", "Re: Deutsche Bank confirms talks on strategic partnership with Sal. Oppenheim Group Have we set up a meeting with them for when I'm in London. Who are we actually talking to? Thanks Jes"]	["EFTA01256081", "EFTA00773396"]
741	Barnaby Marsh	Jeffrey Epstein	8	\N	\N	2	6	["Re: come spend some time in Florida On Thu, May 7, 2009 at 6:13 PM, Bamaby Marsh \\u2022cl wrote: Dear Jeff: I finally heard from Chuck Harper, who is visiting anthropological sites in South Africa at the m", "Re: come spend some time in florida On Thu, May 7, 2009 at 6:13 PM, Barnaby Marsh wrote: Dear Jeff: I finally heard from Chuck Harper, who is visiting anthropological sites in South Africa at the mome", "Re: come spend some time in florida On Thu, May 7, 2009 at 6:13 PM, Barnaby Marsh \\u2039 > wrote: Dear Jeff: I finally heard from Chuck Harper, who is visiting anthropological sites in South Africa at the ", "Re: Science and reality Nice. The questions could be answered if the approach and =ssumptions are at the right breadth and scale; lets", "take a look https://archive.org/details/improvementormin0Owa=tuoft <https://archive.org/details/improvementofmin00w=ttuoft> please note The information contained in this communication is confidential,"]	["EFTA01829009", "EFTA02442393", "EFTA02458867", "EFTA02645293", "EFTA02458577", "EFTA02458897", "EFTA02524641", "EFTA00774801"]
742	Joi Ito	Martin Nowak	4	\N	\N	4	0	["Re:", "Re:", "Re:", "Re:"]	["EFTA00814229", "EFTA01739473", "EFTA00814272", "EFTA01739639"]
743	Janusz Banasiak	Richard Kahn	5	2015-04-16	2017-03-24	4	1	["Re: landscaping", "Fwd: 358 El Brillo Way Res Quote", "Fwd: 358 El Brillo", "Re: landscaping", "Re: Mosquit= Products a> i apologize for short not=ce but would you be able to spray tomorrow at 358 El Brillo Wayau> please advise thank you Richard Kahn"]	["EFTA00859110", "EFTA00819328", "EFTA02662470", "EFTA02452045", "EFTA01051483"]
744	Jean Luc Brunel	Jeffrey Epstein	7	2014-19-11	2015-13-01	0	7	["filed by Brad Edwards who titone sa s ou want to meet with", "how are you holidng up? anyting you woudl like me to do? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside informati", "i tried to call today and ysterdat The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the u", "if you come to the ranch today you can fly with me to la tomorw The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, a", "we will return early sun morning , would you like to come fri ?"]	["EFTA01861372", "EFTA01763304", "EFTA02506534", "EFTA02515358", "EFTA01762879", "EFTA00860929", "EFTA00826353"]
745	Noam Chomsky	Richard Kahn	31	\N	\N	26	5	["taxes", "Fwd: Marital Trusts", "trustees", "Re: Trustees candidates will harry accept either alan halperin at paul weiss or beth tractenburg at steptoe please advise thank you Richard Kahn", "Re: FW: Carol S. Chomsky Marital Trusts - Distribution Acknowledging item 2, as you suggest, is OK except for one qualification. Max writes that he had \\"previously been assured (prior to making tax pa"]	["EFTA00925405", "EFTA00911815", "EFTA01003817", "EFTA00940437", "EFTA01005346", "EFTA00833203", "EFTA00972336", "EFTA00934688", "EFTA00913295", "EFTA01003797"]
746	Bella Klein	Janusz Banasiak	4	2015-04-16	2017-03-24	1	3	["Re: JEFFREY ESPTEIN - HAWB #BRU11407101", "Fwd: 358 El Brillo Way Res Quote", "Fwd: 358 El Brillo", "<=span>Fwd: 358 El Brillo"]	["EFTA00834636", "EFTA00859110", "EFTA01051483", "EFTA02655276"]
747	Darren Indyke	Paul Morris	3	2015-10-01	2015-10-01	3	0	["Re: Mort Inc [C]", "Re: Mort Inc [C] When this happened once before, we agreed that your team would give us notice of any account that was in danger of becoming inactive. I have a", "FW: Mort Inc [C] [I] Classification: For internal use only Paul Morris Managing Director Deutsche Bank Private Bank ML Office: Cell: 9"]	["EFTA01402518", "EFTA00844534", "EFTA01474803"]
748	Bradley Edwards	Jeffrey Epstein	13	\N	\N	1	12	["now? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addresse", "settlement purposes only after much back and forth, language similar to . alan . i was furious and angry , and in the heat of the moment said some things that i wish i hadn't/ ? brad and paul. in hind", "foundation donation", "now? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the addresse", "Re: ok On Fri, Oct 2, 2015 at 12:33 PM, Brad Edwards <brad@pathtojustic=.com <mailto:brad@pathtojustice.com\\u00bb wrote: On another call. Should end aft=r 1. How about 1:30? <image001.png>=/u> Brad Edwards"]	["EFTA02714716", "EFTA02484843", "EFTA02354145", "EFTA02484737", "EFTA01028706", "EFTA02710692", "EFTA02710678", "EFTA02714552", "EFTA01200796", "EFTA01732175"]
749	Paul Morris	Richard Joslin	2	\N	\N	0	2	["RE: KCP Onboarding + Power of Attorney (POA) [C] [1]", "RE: KCP Onboarding + Power of Attorney (POA) [C] [I]"]	["EFTA00857900", "EFTA00857754"]
789	Harry Beller	Jeffrey Epstein	2	\N	\N	0	2	["Re: casli ti didnt we just transfer 500k last week? On Thu, Jan 24, 2013 at 3:00 PM, Harry Beller wrote: Jeffrey", "Re: cash funding didnt we just transfer 500k last week? On Thu, Jan 24, 2013 at 3:00 PM, Harry Beller <harrybeller@gmail.com> wrote: Jeffrey"]	["EFTA01905818", "EFTA01905937"]
794	Andrew Farkas	David Stern	2	\N	\N	0	2	["Re: Andrew,", "Re: Andrew,"]	["EFTA01964149", "EFTA02393868"]
750	Jeffrey Epstein	Kathryn Ruemmler	8	\N	\N	4	4	["dershowitz said that david bois himself met with know him or can find out the truth please note The information contained in this communication is confidential, may be attorney-client privileged, may ", "Re:", "Re:", "Fwd: Paul Simon_CURE_DC_Info (=)", "any luck on amici? should we let main justice know quietly the conseqeuences of an adverse ruling please note The information contained in this communication is confidential, may be attorney-client pr"]	["EFTA00859978", "EFTA02499356", "EFTA02660785", "EFTA00864553", "EFTA02498478", "EFTA00864557", "EFTA02660440", "EFTA02485126"]
751	Jeffrey Epstein	Tancredi Marchiolo	4	\N	\N	3	1	["Nick in NYC Dear Jeffrey, As mentioned earlier my good friend Nick Gordon Smith in copy is coming to NYC mid next month. You guys", "Re: im in paris now who is it? On Fri, May 13, 2016 at 10:44 PM, Tancredi Marchiolo <tmarchiolo@hotmail.co=<mailto: <mailto mailto:tmarc=iolo@hot mail.com\\u00bb<mailto: mailto:tmarchiolo@hotmail=corn>cmail", "Re: will your friend be in paris? On Tue, Jul 26, 2011 at 12:19 PM, Tancredi Marchiolo wrote: Ciao Jeffrey are you in paris/europe from 30th? Let's meet up for a couple of days? This communication, in", "Re: im in paris now who is it? On Fri, May 13, 2016 at 10:44 PM, Tancredi Marchiolo"]	["EFTA02462515", "EFTA02703249", "EFTA00865078", "EFTA02693974"]
752	Cecile de Jongh	Daphne Wallace	6	\N	\N	6	0	["Re: Inspection Request Good morning JP,", "Fw: Work on LSJ Island FYI With warm regards, Cecile Good afternoon JP, Please see the email that I sent to you on Friday at your old email", "Carlton Dowe", "FYI - Summer Schedule With warm regards, Cecile DISCLAIMER: The information contained in this e-mail may be privileged,confidential, and protected from disclosure. If you are not the intended recipien", "Carlton Dowe"]	["EFTA02165048", "EFTA02338856", "EFTA00871210", "EFTA01952803", "EFTA02078405", "EFTA01952859"]
753	Bill Gates	Boris Nikolic	7	\N	\N	3	4	["tmr night! Importance: High Have you ever been in legendary Crazy Horse in Paris?", "tmr night! Importance: High Have you ever been in legendary Crazy Horse in Paris?", "Jeffery - Thank you", "FW:", "Location Are you in DC or somewhere else?"]	["EFTA00967378", "EFTA01966401", "EFTA00873390", "EFTA01762642", "EFTA02573664", "EFTA01953133", "EFTA00873400"]
754	Jeffrey Epstein	Steve Bannon	28	\N	\N	28	0	["Re: Lawyer for Susan Rice: Obama administration justifiably concerned' about sharing intel with Trump team - POLITICO coin issues. : receive coins. distribute coins, pay in coins. coin cooperative. pr", "Did you use the shampoo? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the", "Did you use the shampoo? please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the", "Re: Could be , what are you thinking ? On Sat, Feb 17, 2018 at 2:52 PM Steve Bannon < > wrote: You down in palm beach next week??? On Feb 17, 2018, at 10:05 AM, jeffrey E. leevacation\\u00aegmail.com> wrote", "Re:"]	["EFTA02518894", "EFTA00881543", "EFTA02523277", "EFTA00881250", "EFTA02523051", "EFTA00881717", "EFTA02518578", "EFTA00881619", "EFTA00881171", "EFTA00881711"]
755	Jeffrey Epstein	Mary Erdoes	2	\N	\N	0	2	["Re:", "RE:"]	["EFTA00878237", "EFTA00913831"]
756	Jeffrey Epstein	Marvin Minsky	3	\N	\N	0	3	["Re: Foundation Advisor", "Re: Foundation Advisor", "Re: Foundation Advisor"]	["EFTA02027291", "EFTA02028522", "EFTA00878785"]
757	Isabel Maxwell	Jeffrey Epstein	1	\N	\N	1	0	["Re: Would this mean they wd buy the fish and the coral in the tanks too?? Sent from my iPhone Isabel Maxwell 1310 456 5172 1415 298 0009 mob On Apr 14, 2009, at 9:03 AM, \\"Gmax\\" < > wrote:"]	["EFTA00881200"]
758	Gary Kerney	Richard Kahn	5	\N	\N	3	2	["RE: pool Thank you Funds to be wired today Rich Kahn", "Dejongh Jeffrey When we shut down Gensler I took the kitchen and laundry to Dejongh two weeks ago to get the building permits. He gave me a not to exceed proposal of $11,000 for each,very reasonable, ", "Re: RE: Pay me directly. You have my direct deposit ? Sent from my iPhone On Feb 28, 2011, at 11:13 AM, \\"Rich Kahn' wrote:", "RE: K & S Change order when k&s bid the wind doors the bid was worded as two pair of doors. Shelia the business partner wrote the bid up but using $7,200 the price of one opening.' found this out afte", "RE: pool Thank you Funds to be wired today Rich Kahn"]	["EFTA02412984", "EFTA01849302", "EFTA01779990", "EFTA00898616", "EFTA01800288"]
759	Boris Nikolic	Jean Luc Brunel	2	\N	\N	2	0	["RE: Thank you so much! >; Sam Jaradeh<", "RE: Thank you so much! Thank you Jean Luc! It has been a while since we met. Hope to see you some time"]	["EFTA01834420", "EFTA00902486"]
760	Jeffrey Epstein	Nicholas Ribis	23	\N	\N	18	5	["Re:", "FW: Wiring Instructions", "getting hotter please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of th", "Re: are you on cell? On Sat, May 27, 2017 at 6:14 PM, Nicholas Ribis < wrote: Wow I wonder what Jarred did u know DJT knew!", "Re: ping me when awake On Sat, May 27, 2017 at 6:23 PM, Nicholas Ribis < wrote: Yes but bad time call me at 8 or early tomorrow"]	["EFTA02638534", "EFTA02543698", "EFTA02647764", "EFTA01042937", "EFTA01044364", "EFTA02395183", "EFTA01044538", "EFTA02395441", "EFTA02647452", "EFTA00911079"]
761	Lesley Groff	Mary Erdoes	1	\N	\N	0	1	["RE:"]	["EFTA00913831"]
762	Bradley Edwards	Lesley Groff	7	2011-08-02	2011-08-02	0	7	["Jeffrey Epstein", "Jeffrey Epstein", "Jeffrey Epstein EFTA00917505", "Jeffrey Epstein", "Jeffrey Epstein EFTA_R1_00479248 EFTA01987763"]	["EFTA01857408", "EFTA01987762", "EFTA00915997", "EFTA00917459", "EFTA00917504", "EFTA02185307", "EFTA01994809"]
763	Daphne Wallace	Gary Kerney	1	2011-07-28	2011-07-28	1	0	["As requested - July 28, 2011 Greetings Gary, As requested. DW The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and"]	["EFTA00918384"]
764	Barry Josephson	Richard Kahn	4	\N	\N	0	4	["Promissory Note < I have attached a schedule of payments and balance outstanding with interest as of 9/15/2011", "Promissory Note I have attached a schedule of payments and balance outstanding with interest as of 9/15/2011", "Promissory Note I have attached a schedule of payments and balance outstanding with interest as of 9/15/2011", "Promissory <imatief 241 IN> I have attached a schedule of payments and balance outstanding with interest as of 9/15/2011"]	["EFTA01855305", "EFTA01857172", "EFTA00919163", "EFTA02036482"]
765	Dana	Richard Kahn	3	\N	\N	3	0	["FW: car Hi Rich,", "car Hi Rich, Ghislaine said that she will take $33k for the Escalade (please see email", "FW: car Hi Rich, Ghislaine said that she will take $33k for the Escalade (please see email"]	["EFTA00921514", "EFTA01853805", "EFTA01989970"]
790	Lesley Groff	Matthew I. Menchel	2	\N	\N	2	0	["Jeffrey Epstein EFTA_R1_00354127 EFTA01915133", "Re: Jeffrey Epstein Got it! Thanks Sent from my iPhone On May 26, 2012 at 12:49 PM \\"Matthew I. Menchel\\" wrote:"]	["EFTA01915132", "EFTA02167941"]
766	Cecile de Jongh	Lawrence Krauss	5	\N	\N	3	2	["Future in Computin Conference - St. John, Virgin Islands Reply-To: Cecile de Jongh >. Wo'cik Michael Hello Everyone, > >, Barnaby Re: Future in Computing  Conference sponsored by the J. Epstein VI Fou", "Future in Computing Conference - St. John, Virgin Islands > vrence Krauss < >. Barnaby Marsh Wo cik Michael < Hello Everyone, Re: Future in Computing  Conference sponsored by the J. Epstein VI Foundat", "Re: Re: We are having a series of internal meetings this week and the agenda will depend upon them somewhat so that would be difficult. I could", "Re: Re: EFTA_R1_00474406 EFTA01984385", "Re: agenda revised Hi Lawrence, The agenda seems to be shaping up. I recall that several people do not arrive until after 8 PM on Friday. I have sent Judi all the itineraries that we have thus far. Yo"]	["EFTA02420555", "EFTA01984336", "EFTA01984384", "EFTA00924646", "EFTA00924092"]
767	Boris Nikolic	Richard Kahn	5	\N	\N	5	0	["RE: Hi Wendy, Can you please help Richard with a transfer of one of our tickets to Jeffrey Epstein to attend TED 2012? Thank you! B The information contained in this communication is confidential, may", "RE: Hi Wendy, Can you please help Richard with a transfer of one of our tickets to Jeffrey Epstein to attend TED 2012? Thank you! B EFTA_R1_00233145 EFTA01844562", "RE: Hi Wendy, Can you please help Richard with a transfer of one of our tickets to Jeffrey Epstein to attend TED 2012? Thank you! B *********************************************************** The info", "RE: Hi Wendy, Can you please help Richard with a transfer of one of our tickets to Jeffrey Epstein to attend TED 2012? Thank you! B EFTA_R1_00529668 EFTA02023181", "RE: <=span> Hi=Wendy, <=span> Can =ou please help Richard with a transfer of one of our tickets to Jeffrey Ep=tein to attend TED 2012? =hank you! B =/html>= 2 EFTA_R1_01302863 EFTA02339617"]	["EFTA01844561", "EFTA01844630", "EFTA02023180", "EFTA02339616", "EFTA00928591"]
768	Carluz Toylo	Richard Kahn	12	2017-12-11	2019-03-12	10	2	["PB Cabana area updates", "Re: Dock steps near Cabana", "Re: Work Plan Front Steps El Brillo Entrance / Pool Entrance", "Re: FBI Garage", "pavers"]	["EFTA01033359", "EFTA02622722", "EFTA02666025", "EFTA01021717", "EFTA00947769", "EFTA00947590", "EFTA01058399", "EFTA02623846", "EFTA01024304", "EFTA01017898"]
769	Danny Vicars	Daphne Wallace	1	\N	\N	1	0	["Fw: hi pot testing"]	["EFTA00950516"]
770	Paul Krassner	Richard Kahn	1	2017-08-02	2017-08-02	0	1	["Re: Subject to change"]	["EFTA00957112"]
771	Bradley Edwards	Sigrid McCawley	1	\N	\N	0	1	["RE: Epstein Hello Tonja, Boies Schiller will be representing as a non-party witness at her deposition in this action. As testimony may implicate sensitive issues o we are requesting your agreement tha"]	["EFTA01003719"]
772	Jack Scarola	Sigrid McCawley	1	\N	\N	0	1	["RE: Epstein Hello Tonja, Boies Schiller will be representing as a non-party witness at her deposition in this action. As testimony may implicate sensitive issues o we are requesting your agreement tha"]	["EFTA01003719"]
773	Ann Rodriguez	Daphne Wallace	1	\N	\N	1	0	["Re: Quotation of Landscape light led solar light garden from Quanzhou Innovation to Ann Rodriquez Hi Fancy Lv,"]	["EFTA01011009"]
774	Ann Rodriguez	Richard Kahn	1	\N	\N	1	0	["Re: Quotation of Landscape light led solar light garden from Quanzhou Innovation to Ann Rodriquez Hi Fancy Lv,"]	["EFTA01011009"]
775	Harry Fisch	Jeffrey Epstein	2	\N	\N	1	1	["harry boris, boris harry please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the", "Fwd: confidential\\u2014analysis you asked for. Sent from my iPhone EFTA_R1_00026805 EFTA01738881"]	["EFTA01017946", "EFTA01738880"]
776	Jeffrey Epstein	Robert Trivers	2	\N	\N	0	2	[]	["EFTA02660888", "EFTA01055196"]
777	Harry Beller	Richard Kahn	7	2013-11-12	2014-01-14	1	6	["re: 1-14-2014 \\" \\u2022 ' all back is not necessary[attachment .pdf\\" deleted by Amanda Kirby/db/dbcom] thank you Richard Kahn", "re: wire 11-19-2013 Please call Harry to confirm Thank you[attachment \\"DBJEE Euros_WT_M Damien Vannieenwenhove_11-19-2013.pdf\\" deleted by Amanda Kirby/db/dbcom] Richard Kahn", "re: wires (4) 12-11-2013 Please call Harry to confirm Can you please try to send out 225k and 10k wires today m isk Thank you[attachment \\"HE DB_WT_Larr Visoski 12-11-2013.pdf\\" deleted by tiage/db/dbco", "Re: wires (4) 1-9-2014 thank you Richard Kahn", "Fwd: wires (2) 5-30-2013 can you please review wire that was sent yesterday to Jet Ups LLC i believe that you sent 1500 vs 4500 on instructions thank you Richard Kahn"]	["EFTA01589783", "EFTA01590816", "EFTA01405013", "EFTA01769047", "EFTA01400939", "EFTA01401674", "EFTA01401692"]
778	Bella Klein	Brice Gordon	3	\N	\N	2	1	["RE: LSJE wire to", "LSJE xxx9295 wire to ; Stewart Oldfield", "Fwd: Aspen Landscaping EFTA_R1_00503736 EFTA02005135"]	["EFTA01436137", "EFTA02005134", "EFTA01411821"]
779	Bella Klein	Paul Morris	8	2014-05-13	2014-09-29	8	0	["JE WT to RB Please confirm,", "JE WT to RB Please confirm,", "Re: Checks Update [C] - Zorro Development Corporation Checks Were delivered to VI office, unfortunately it is not what we ordered'''''' It is personal checks, not for Quick books! Margaux, please requ", "Re: Checks Update [C] - Zorro Development Corporation Checks Were delivered to VI office, unfortunately it is not what we ordered'''''' It is personal checks, not for Quick books! Margaux, please re u", "Fwd: 2 wires Paul, I did not receive confirmation from Amanda on the attached 2 wires. Please"]	["EFTA01477054", "EFTA01472206", "EFTA01468805", "EFTA01468810", "EFTA01474726", "EFTA01411863", "EFTA01477057", "EFTA01412104"]
780	Dana	Jeffrey Epstein	5	\N	\N	5	0	["Trans instructions Attachments: Samantha Harris Transfer July (2nd) 2012.pdf Hi Gina, I have received the fax which Ghislaine needs to sign for paperless", "Transfer Attachments: Samantha Harris Transfer July 2012.pdf Good morning, Gina", "Maxwell transfer Attachments: Transfer Payment to Samantha Harris (Invoice #001).pdf Hi Gina,", "Transfer request from Ghislaine Attachments: VividMinds Retainer Transfer September 2012.pdf Hi Gina,", "Transfer request Attachments: VividMinds Transfer August 2012 (2).pdf"]	["EFTA01589048", "EFTA01588773", "EFTA01588896", "EFTA01588763", "EFTA01589058"]
781	Bella Klein	Harry Beller	1	\N	\N	1	0	["JEE WT to Attachments: SKMBTCRIIIIIIIIIIRtf; ATT00001.htm"]	["EFTA01589374"]
782	Danny Hillis	Jeffrey Epstein	4	\N	\N	0	4	["<no subject> when are you next in ny? The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for th", "Re: PED On Fri, Dec 5, 2014 at 9:43 AM, Danny Hillis < <mailto > wrote: Btw, Larry Summers seems really smart, but I was surprised about how"]	["EFTA02597179", "EFTA02598927", "EFTA02596983", "EFTA01754301"]
783	Dana	Larry Visoski	1	\N	\N	0	1	["Denver Aspen Hi, Appears you need to depart Denver at 3pm to arrive Aspen lhour before sunset due to flight options regs, I believe yor flight arrives Denver at 330pm, so departur to Aspen not possibl"]	["EFTA01771137"]
784	Jeffrey Epstein	Sultan Ahmed bin Sulayem	1	\N	\N	1	0	[]	["EFTA01771347"]
795	Boris Nikolic	Eva Dubin	1	\N	\N	0	1	["RE: Boris, are you planning to call the doctors or Bill or his father 7 Maybe you want to speak to a few ENT specialists 7"]	["EFTA01980362"]
796	Al Seckel	Gerald Sussman	1	\N	\N	0	1	["May I ask you to bring one more gift please?"]	["EFTA02001025"]
797	Gary Kerney	Janusz Banasiak	1	\N	\N	0	1	["pictures Here there arc, missing EFTA_R1_00534846 EFTA02026785"]	["EFTA02026784"]
798	Lesley Groff	Michael Wolff	1	\N	\N	1	0	["Re: Meeting or call w/ Jeffrey"]	["EFTA02033063"]
799	Ariane de Rothschild	Lesley Groff	1	\N	\N	0	1	["Fwd: N212JE I SKBO Handling Info 1 116012395 Please see below and attached from our pilot Larry Visoski...Also La Visoski's cell is ..could we please have a contact cell number on your end? Thank you,"]	["EFTA02065367"]
800	Cecile de Jongh	Richard Kahn	2	2015-10-06	2015-10-06	2	0	["Re: STC computer", "e: computer"]	["EFTA02071720", "EFTA02071764"]
801	Larry Visoski	Lisa Randall	2	\N	\N	2	0	["Re: info for flight", "Re: i=fo for flight"]	["EFTA02300458", "EFTA02089802"]
802	Lesley Groff	Woody Allen	1	\N	\N	0	1	["Car in Paris Hi Lesley, Jeffrey told Soon-Yi that they could use his driver in Paris. Are you able to give him the info, or would you like me to call him? Whatever it's easier for you! Gini please not"]	["EFTA02104850"]
803	Lesley Groff	Nicole Junkermann	8	\N	\N	8	0	["Fwd: Rome to Berlin Hello Nicole. How kind of you to help out here. Please let me know once you have coordinated the car and how I can get payment to you or the", "Fwd: Rome to Berlin Hello Nicole. How kind of you to help out here. Please let me know once you have coordinated the car and how I can get payment to you or the", "Fwd: Rome to Berlin Hello Nicole. How kind of you to help out here. Please let me know once you have coordinated the car and how I", "Fwd: Rome to Berlin Hello Nicole. How kind of you to help out here. Please let me know once you have coordinated the car and how I", "Fwd: Rome to Berlin Hello Nicole. How kind of you to help out here. Please let me know once you have coordinated the car and how I can get payment to you or the"]	["EFTA02136334", "EFTA02136308", "EFTA02136321", "EFTA02136565", "EFTA02135243", "EFTA02135473", "EFTA02135565", "EFTA02135813"]
804	Lesley Groff	Nathan Wolfe	2	\N	\N	0	2	["Re: Je rey ps e n 130 is perfect. See you tomorrow! On Wednesday, February 20, 2013, Lesley Groff wrote: Hello Nathan...I understand you will be in NY this Friday Feb. 22...might you be available to c", "Re: Jeffrey Epstein 130 is perfect. See you tomorrow! On Wednesday, February 20, 2013, Lesley Groff wrote: Hello Nathan...I understand you will be in NY this Friday Feb. 22...might you be available to"]	["EFTA02147105", "EFTA02146610"]
805	Lesley Groff	Steven Sinofsky	1	\N	\N	1	0	["Re: Jeffrey Epstein tremendous...thanks for your help! Hi Steve! Make it 8:30pm tonight to Jeffrey's home please...he lives at: 9 East 71st Street between 5th and Madison If you need to call the house"]	["EFTA02147449"]
806	Howard Lutnick	Lesley Groff	1	\N	\N	0	1	["Jeffrey Epstein Hello Mr. Lutnick. Jeffrey Epstein understands you will be down in St. Thomas some over the holidays. Jeffrey requested I please pass along some"]	["EFTA02151356"]
807	Cecile de Jongh	Una Pascal	1	\N	\N	1	0	["FYI - Summer Schedule With warm regards, Cecile DISCLAIMER: The information contained in this e-mail may be privileged,confidential, and protected from disclosure. If you are not the intended recipien"]	["EFTA02165048"]
808	Barry Josephson	Lesley Groff	1	\N	\N	0	1	["Re: Jeffrey Epstein Hi Barry. Checking in. ... what do you think about a set visit today or tomorrow? Lesley Sent from my iPhone On Mar 13, 2017, at 11:47 AM, Barry Josephson wrote: Exactly. We'll be "]	["EFTA02207509"]
809	Kenneth Starr	Lesley Groff	1	\N	\N	0	1	["Jeffreci n Hello Ken! The best address to send a preview copy of your book to for Jeffrey will be his home in NY...we can then fed ex to him no matter where he is...! Jeffrey Epstein 9 East 71st Stree"]	["EFTA02256340"]
810	Karyna Shuliak	Tom Pritzker	1	\N	\N	1	0	["Re: RE: Re: Thank you very much for your help!! 8,at6:36 PM, Pritzker, Tom > wrote: Thx Sent from my iPad On Apr 6, 2018, at 11:15 AM, Jeskewitz, Jeannine > wrote:<=p> I'm in touch wi=Mand Karyna, we "]	["EFTA02305806"]
811	Doug Schoettle	Emad Hanna	1	\N	\N	0	1	["fan Jeffrey, I didn't ask for approval because its within Gary's approval rate Below is what the fan looks like <image001.png> Thank you Emad Hanna Project Controller HBRK Associates 2 EFTA_R1_0122514"]	["EFTA02318588"]
812	Doug Band	Ghislaine Maxwell	1	\N	\N	1	0	["Re: Just grabbing a quick bite at diner next to my house Going out with sieve bing later Tired and feeling poopsy Grt seeing you as well"]	["EFTA02333083"]
813	Andrew Farkas	David Mitchell	1	\N	\N	1	0	["Re:"]	["EFTA02378730"]
814	George Stephanopoulos	Peggy Siegal	1	\N	\N	0	1	["Thursday small dinner for Prince Andrew George: do not think less of me but I am putting together a very last minute casual dinner for Prince Andrew, who is"]	["EFTA02411832"]
815	Leon Black	Lesley Groff	1	\N	\N	0	1	["Jeffrey Epstein Hello Leon! Jeffrey would like to know what he should do with the 2,352,941 shares of Environmental Solutions Worldwide, Inc that FTC purchased in April of 2005? Please let me know! Th"]	["EFTA02441323"]
816	Ashley	Jeffrey Epstein	1	\N	\N	1	0	["Epstei="]	["EFTA02495432"]
817	Jeffrey Epstein	Soon-Yi Previn	1	2015-05-04	2015-05-04	0	1	["Fwd: Thursday dinner"]	["EFTA02502921"]
818	Jeffrey Epstein	Wallace Cunningham	1	\N	\N	1	0	["should we consider a large glass building to the east of the pool, 20 feet. blocking the wind, alllwoing the view. if we sink it a bit the furniture inside will not block the view.? sun area. ? views "]	["EFTA02510147"]
819	Jeffrey Epstein	Svetlana	1	\N	\N	1	0	["Fwd:"]	["EFTA02542614"]
820	Austin Hill	Lesley Groff	1	\N	\N	0	1	["Re: Retainer & Invoicing for our project with Jeffrey"]	["EFTA02568748"]
821	Michael Wolff	Steve Bannon	1	\N	\N	1	0	["How's it looking...? lemme know > > 2 EFTA_R1_01770201 EFTA02589080"]	["EFTA02589079"]
822	Jeffrey Epstein	Miroslav Lajcak	1	\N	\N	1	0	["Re: Vacation For most shows On Fri, Jul 20, 2018 at 10:59 AM jeffrey E. <jeevacation@gmail.com&=t; wrote: Go through july 29 las vegas shows. Cirque de soleil etc = get free tickets On Fri, Jul 20, 20"]	["EFTA02604049"]
823	Boris Nikolic	Harry Fisch	2	\N	\N	2	0	["RE: Thank you JI Great meeting you Harry!", "RE: Thank you J! Great meeting you Harry!"]	["EFTA02617195", "EFTA02617256"]
824	Jeffrey Epstein	Valdson Cotrin	1	\N	\N	0	1	["Fuite salle de bain Mr Epstein."]	["EFTA02617939"]
825	Jeffrey Epstein	Richard Axel	1	\N	\N	1	0	["Boris/Richard please note The information contained in this communication is confidential, may be attorney-client privileged, may constitute inside information, and is intended only for the use of the"]	["EFTA02623752"]
826	Daphne Wallace	Erika Kellerhals	1	\N	\N	1	0	[]	["EFTA02625888"]
827	Richard Kahn	Una Pascal	1	\N	\N	0	1	["<=span>Fwd: LSJE_PAYROLL_052818"]	["EFTA02655898"]
828	Danny Vicars	Richard Kahn	1	\N	\N	0	1	["Re: NEW DATES ORDER#2-1-2017-001 not sure what that means has it shipped from France? if so tracking number? if not when will it ship and please obtain a tracking =umber is it shipping directly to STT"]	["EFTA02657196"]
829	Danny Vicars	Jeffrey Epstein	1	\N	\N	1	0	["Fw: Water softener"]	["EFTA02657471"]
830	Brice Gordon	Larry Visoski	1	\N	\N	1	0	[]	["EFTA02716449"]
\.


--
-- Data for Name: entities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.entities (id, name, entity_type, source_id, source_table, aliases, metadata, mention_count, created_at) FROM stdin;
1	Jeffrey Epstein	person	1	persons	\N	{"occupation": "Financier", "person_type": "perpetrator", "legal_status": "deceased", "public_figure": true, "ds10_mention_count": 3687}	0	2026-02-05 22:53:03
2	Ghislaine Maxwell	person	2	persons	\N	{"occupation": "Socialite", "person_type": "perpetrator", "legal_status": "convicted", "public_figure": true, "ds10_mention_count": 181}	0	2026-02-05 22:53:03
3	Leon Black	person	3	persons	\N	{"source": "ds10_analysis", "occupation": "Private equity, Apollo Global Management", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; multiple victim allegations of sexual assault and trafficking; also alleged present during abuses with Barr", "person_type": "associate", "legal_status": "no_action", "public_figure": true, "ds10_mention_count": 14}	0	2026-02-05 22:53:03
4	Jes Staley	person	4	persons	\N	{"source": "ds10_analysis", "occupation": "Banker, former Barclays CEO", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; victim allegation of forced sexual assault during massage", "person_type": "associate", "legal_status": "no_action", "public_figure": true, "ds10_mention_count": 14}	0	2026-02-05 22:53:03
5	Les Wexner	person	5	persons	\N	{"source": "ds10_analysis", "occupation": "Retail executive, L Brands", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; victim allegation of financial/personal relationship", "person_type": "associate", "legal_status": "no_action", "public_figure": true, "ds10_mention_count": 4}	0	2026-02-05 22:53:03
6	Prince Andrew	person	6	persons	\N	{"source": "ds10_analysis", "occupation": "British Royal, Duke of York", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; multiple allegations including witness corroboration", "person_type": "associate", "legal_status": "settled", "public_figure": true, "ds10_mention_count": 14}	0	2026-02-05 22:53:03
7	Alan Dershowitz	person	7	persons	\N	{"source": "ds10_analysis", "occupation": "Attorney, Harvard Law Professor", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; victim allegation of massage on plane (victim noted as not a minor)", "person_type": "associate", "legal_status": "no_action", "public_figure": true, "ds10_mention_count": 7}	0	2026-02-05 22:53:03
8	Glenn Dubin	person	8	persons	\N	{"occupation": "Hedge fund manager", "person_type": "associate", "legal_status": "no_action", "public_figure": true, "ds10_mention_count": 2}	0	2026-02-05 22:53:03
9	Jean-Luc Brunel	person	9	persons	\N	{"occupation": "Model agent", "person_type": "perpetrator", "legal_status": "deceased", "public_figure": true}	0	2026-02-05 22:53:03
10	Sarah Kellen	person	10	persons	\N	{"occupation": "Assistant", "person_type": "enabler", "legal_status": "no_action", "public_figure": true}	0	2026-02-05 22:53:03
11	Nadia Marcinkova	person	11	persons	\N	{"occupation": "Assistant", "person_type": "enabler", "legal_status": "no_action", "public_figure": true}	0	2026-02-05 22:53:03
12	Lesley Groff	person	12	persons	\N	{"occupation": "Executive assistant", "person_type": "enabler", "legal_status": "no_action", "public_figure": true, "ds10_mention_count": 1008}	0	2026-02-05 22:53:03
13	Bill Clinton	person	13	persons	\N	{"source": "ds10_analysis", "occupation": "Former US President", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; FBI noted not a victim in case; allegation of orgy invitation (not attended)", "person_type": "associate", "legal_status": "no_action", "public_figure": true, "ds10_mention_count": 12}	0	2026-02-05 22:53:03
14	Donald Trump	person	14	persons	\N	{"source": "ds10_analysis", "occupation": "Businessman/Politician", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; victim allegations of sexual abuse", "person_type": "mentioned", "legal_status": "no_action", "public_figure": true, "ds10_mention_count": 16}	0	2026-02-05 22:53:03
15	Harvey Weinstein	person	15	persons	\N	{"source": "ds10_analysis", "occupation": "Film producer", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; multiple victim allegations of massage coercion and sexual assault", "person_type": "associate", "legal_status": "convicted", "public_figure": true, "ds10_mention_count": 0}	0	2026-02-05 22:53:03
16	Epstein	person	16	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 8326}	0	2026-02-05 22:53:03
17	Maxwell	person	17	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 456}	0	2026-02-05 22:53:03
18	Black	person	18	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 773}	0	2026-02-05 22:53:03
19	Ross	person	19	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 285}	0	2026-02-05 22:53:03
20	Trump	person	20	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 114}	0	2026-02-05 22:53:03
21	Clinton	person	21	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 20}	0	2026-02-05 22:53:03
22	President Clinton	person	22	persons	\N	{"person_type": "unknown", "legal_status": "unknown"}	0	2026-02-05 22:53:03
23	Andrew	person	23	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 152}	0	2026-02-05 22:53:03
24	Dershowitz	person	24	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 11}	0	2026-02-05 22:53:03
25	Weinstein	person	25	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 6}	0	2026-02-05 22:53:03
26	Ms. Maxwell	person	26	persons	\N	{"person_type": "unknown", "legal_status": "unknown"}	0	2026-02-05 22:53:03
27	Alessi	person	27	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
28	Indyke	person	28	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 364}	0	2026-02-05 22:53:03
29	Kahn	person	29	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1075}	0	2026-02-05 22:53:03
30	Jeffrey E. Epstein	person	30	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 4}	0	2026-02-05 22:53:03
31	Richard D. Kahn	person	31	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
32	Darren K. Indyke	person	32	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 15}	0	2026-02-05 22:53:03
33	Gates	person	33	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 13}	0	2026-02-05 22:53:03
34	Groff	person	34	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1753}	0	2026-02-05 22:53:03
35	EPSTEIN	person	35	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 8326}	0	2026-02-05 22:53:03
36	JEFFREY EPSTEIN	person	36	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 3687}	0	2026-02-05 22:53:03
37	ross	person	37	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 285}	0	2026-02-05 22:53:03
38	rOSS	person	38	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 285}	0	2026-02-05 22:53:03
39	Richard Kahn	person	39	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 496}	0	2026-02-05 22:53:03
40	epstein	person	40	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 8326}	0	2026-02-05 22:53:03
41	gates	person	41	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 13}	0	2026-02-05 22:53:03
42	GHISLAINE MAXWELL	person	42	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 181}	0	2026-02-05 22:53:03
43	MAXWELL	person	43	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 456}	0	2026-02-05 22:53:03
44	black	person	44	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 773}	0	2026-02-05 22:53:03
45	ROSS	person	45	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 285}	0	2026-02-05 22:53:03
46	INDYKE	person	46	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 364}	0	2026-02-05 22:53:03
47	DARREN INDYKE	person	47	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 145}	0	2026-02-05 22:53:03
48	ePstein	person	48	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 8326}	0	2026-02-05 22:53:03
49	maxwell	person	49	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 456}	0	2026-02-05 22:53:03
50	Juan Alessi	person	50	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
51	trump	person	51	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 114}	0	2026-02-05 22:53:03
52	andrew	person	52	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 152}	0	2026-02-05 22:53:03
53	JEFFREY E. EPSTEIN	person	53	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 4}	0	2026-02-05 22:53:03
54	BLACK	person	54	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 773}	0	2026-02-05 22:53:03
55	Duke of York	person	55	persons	\N	{"person_type": "unknown", "legal_status": "unknown"}	0	2026-02-05 22:53:03
56	GATES	person	56	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 13}	0	2026-02-05 22:53:03
57	DARREN K. INDYKE	person	57	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 15}	0	2026-02-05 22:53:03
58	dershowitz	person	58	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 11}	0	2026-02-05 22:53:03
59	jeffrey epstein	person	59	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 3687}	0	2026-02-05 22:53:03
60	Jeffrey epstein	person	60	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 3687}	0	2026-02-05 22:53:03
61	JEFFREY Epstein	person	61	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 3687}	0	2026-02-05 22:53:03
62	Brunel	person	62	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 33}	0	2026-02-05 22:53:03
63	Wexner	person	63	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 16}	0	2026-02-05 22:53:03
64	KAHN	person	64	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1075}	0	2026-02-05 22:53:03
65	RICHARD D. KAHN	person	65	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
66	ANDREW	person	66	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 152}	0	2026-02-05 22:53:03
67	Darren Indyke	person	67	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 145}	0	2026-02-05 22:53:03
68	GhISLAINE MAXWELL	person	68	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 181}	0	2026-02-05 22:53:03
69	Jeffrey EPSTEIN	person	69	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 3687}	0	2026-02-05 22:53:03
70	prince Andrew	person	70	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 14}	0	2026-02-05 22:53:03
71	Staley	person	71	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 29}	0	2026-02-05 22:53:03
72	weinstein	person	72	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 6}	0	2026-02-05 22:53:03
73	truMp	person	73	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 114}	0	2026-02-05 22:53:03
74	GHiSLAINE MAXWELL	person	74	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 181}	0	2026-02-05 22:53:03
75	MS. MAXWELL	person	75	persons	\N	{"person_type": "unknown", "legal_status": "unknown"}	0	2026-02-05 22:53:03
76	GIUFFRE	person	76	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 7}	0	2026-02-05 22:53:03
77	Bill Gates	person	77	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
78	Jeffrey E. EPSTEIN	person	78	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 4}	0	2026-02-05 22:53:03
79	Darren K. INDYKE	person	79	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 15}	0	2026-02-05 22:53:03
80	Darren INDYKE	person	80	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 145}	0	2026-02-05 22:53:03
81	Dubin	person	81	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 64}	0	2026-02-05 22:53:03
82	Glen Dubin	person	82	persons	\N	{"source": "ds10_analysis", "occupation": "Hedge fund manager", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; victim allegation of massage directed by Maxwell; also trust beneficiary", "person_type": "associate", "legal_status": "unknown", "public_figure": true, "ds10_mention_count": 14}	0	2026-02-05 22:53:03
83	ghislaine maxwell	person	83	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 181}	0	2026-02-05 22:53:03
84	Ghislaine MAXWELL	person	84	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 181}	0	2026-02-05 22:53:03
85	Giuffre	person	85	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 7}	0	2026-02-05 22:53:03
86	giuffre	person	86	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 7}	0	2026-02-05 22:53:03
87	prince andrew	person	87	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 14}	0	2026-02-05 22:53:03
88	wexner	person	88	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 16}	0	2026-02-05 22:53:03
89	clinton	person	89	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 20}	0	2026-02-05 22:53:03
90	ms. Maxwell	person	90	persons	\N	{"person_type": "unknown", "legal_status": "unknown"}	0	2026-02-05 22:53:03
91	DERSHOWITZ	person	91	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 11}	0	2026-02-05 22:53:03
92	ALAN DERSHOWITZ	person	92	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 7}	0	2026-02-05 22:53:03
93	EpStein	person	93	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 8326}	0	2026-02-05 22:53:03
94	LEON BLACK	person	94	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 14}	0	2026-02-05 22:53:03
95	weInstein	person	95	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 6}	0	2026-02-05 22:53:03
96	STALEY	person	96	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 29}	0	2026-02-05 22:53:03
97	indyke	person	97	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 364}	0	2026-02-05 22:53:03
98	brunel	person	98	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 33}	0	2026-02-05 22:53:03
99	roSS	person	99	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 285}	0	2026-02-05 22:53:03
100	JES STALEY	person	100	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 14}	0	2026-02-05 22:53:03
101	kahn	person	101	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 1075}	0	2026-02-05 22:53:03
102	MaxwelL	person	102	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 456}	0	2026-02-05 22:53:03
103	WEXNER	person	103	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 16}	0	2026-02-05 22:53:03
104	VIRGINIA ROBERTS	person	104	persons	\N	{"person_type": "unknown", "legal_status": "unknown"}	0	2026-02-05 22:53:03
105	staley	person	105	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 29}	0	2026-02-05 22:53:03
106	Maria Alessi	person	106	persons	\N	{"person_type": "unknown", "legal_status": "unknown"}	0	2026-02-05 22:53:03
107	Eva Dubin	person	107	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 29}	0	2026-02-05 22:53:03
108	ClInton	person	108	persons	\N	{"person_type": "unknown", "legal_status": "unknown", "ds10_mention_count": 20}	0	2026-02-05 22:53:03
109	Matt Grippi	person	109	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
110	Alan Greenberg	person	110	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
111	Kathy Greenberg	person	111	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
112	Sophie Biddle	person	112	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
113	Gwendolyn Beck	person	113	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
114	Chuck Schumi	person	114	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
115	David Anton	person	115	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
116	Deborah ?	person	116	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
117	Sharon Reynolds	person	117	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
118	Jim Cayne	person	118	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
119	Patricia Cayne	person	119	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
120	Alison Cayne	person	120	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
121	Warren ?	person	121	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
122	Karv Deweidy	person	122	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
123	Passenger (1)	person	123	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
124	Maria ?	person	124	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
125	Diedri Neal	person	125	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
126	Christine ?	person	126	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
127	Hazell-Iveagh, Clare	person	127	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
128	Frances ?	person	128	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
129	Passenger (4)	person	129	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
130	Passenger (3)	person	130	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
131	Elizabeth Elizabeth	person	131	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
132	A Teal	person	132	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
133	J Teal	person	133	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
134	O Teal	person	134	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
135	Catherine Finglas	person	135	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
136	Pamela Johanaoff	person	136	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
137	Katherina Kotzig	person	137	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
138	Ankie ?	person	138	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
139	Allison ?	person	139	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
140	Cheree ?	person	140	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
141	Tiffany ?	person	141	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
142	Celona ?	person	142	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
143	Passengers, No No Passengers	person	143	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
144	Ira Zicherman	person	144	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
145	Celina ?	person	145	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
146	Andy ?	person	146	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
147	Mandy ?	person	147	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
148	Ralph ?	person	148	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
149	David Rothman	person	149	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
150	Felicia Taylor	person	150	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
151	Passenger (2)	person	151	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
152	Celina Midelfart	person	152	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
153	Robin Plant	person	153	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
154	John Glenn	person	154	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
155	Cazaudumec, Didier	person	155	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
156	Darren ?	person	156	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
157	Jeff Schantz	person	157	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
158	Larry ?	person	158	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
159	Shannon ?	person	159	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
160	Joel Pashcow	person	160	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
161	Sharon ?	person	161	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
162	Andy Stewart	person	162	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
163	Leslie Gelb	person	163	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
164	Brian Mathis	person	164	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
165	Lester Pollack	person	165	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
166	Stephen ?	person	166	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
167	Sophie ?	person	167	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
168	Jeff Shantz	person	168	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
169	Clair ?	person	169	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
170	David Roth	person	170	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
171	Joe ?	person	171	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
172	Nathan Myarold	person	172	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
173	Bran ?	person	173	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
174	Nathan Myhrbold	person	174	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
175	Karen ?	person	175	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
176	Amanda ?	person	176	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
177	Anthony Barrett	person	177	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 3}	0	2026-02-05 22:53:03
178	Anton ?	person	178	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
179	Lynn Forester	person	179	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 2}	0	2026-02-05 22:53:03
180	Ben Forester	person	180	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
181	JoJo ?	person	181	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
182	Bob ?	person	182	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
183	Gary Kervey	person	183	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
184	Donna ?	person	184	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
185	Pamela Stevens	person	185	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
186	Suzanna ?	person	186	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
187	Deidre ?	person	187	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
188	Kathrina ?	person	188	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
189	Lynn ?	person	189	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
190	Lisa ?	person	190	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
191	Nadia ?	person	191	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
192	Jack Robertson	person	192	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
193	Ginger Southgate	person	193	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
194	Heather Mann	person	194	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
195	Steve Tuckerman	person	195	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
196	Judy Tuckerman	person	196	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
197	Yehura Koppel	person	197	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
198	Zipora Koppel	person	198	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
199	Dougle Shouetle	person	199	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
200	Alberto Pinto	person	200	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 5}	0	2026-02-05 22:53:03
201	Pascal ?	person	201	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
202	Gabrielle ?	person	202	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
203	Emmy Tayler	person	203	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
204	Gary Kerney	person	204	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 25}	0	2026-02-05 22:53:03
205	Mary Kerney	person	205	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
206	Joe Pacano	person	206	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
207	Gene ?	person	207	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
208	Manny ?	person	208	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
209	Mandy Ellison	person	209	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
210	Warren Spector	person	210	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
211	Warren Whippet	person	211	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
212	Margaret Whippet	person	212	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
213	Doug Schoettle	person	213	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 6}	0	2026-02-05 22:53:03
214	Sherrie Crape	person	214	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
215	Ellen Spencer	person	215	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
216	Lauren Pashcow	person	216	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
217	Kit Layborne	person	217	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
218	Gary Blackwell (Pilot)	person	218	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
219	Passenger (0) Test Flight	person	219	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
220	Heather Mitchell	person	220	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
221	Andrew Mitchell	person	221	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
222	Melinda Luntz	person	222	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
223	(ROXEBY	person	223	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
725	Daphne Wallace	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
224	Paul Mellon	person	224	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
225	Carolyn ?	person	225	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
226	Oliver Sachs	person	226	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
227	Robin ?	person	227	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
228	Sarah Ferguson	person	228	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
229	TIX Titusville, FL, United States	person	229	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
230	X21 West Palm Beach, FL, United States	person	230	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
231	CRG Titusville, FL, United States	person	231	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
232	PBI Lakeland, FL, United States	person	232	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
233	Ginger ?	person	233	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
234	Mandy Lang	person	234	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
235	Cocoa Brown	person	235	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
236	Linda Pinto	person	236	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 2}	0	2026-02-05 22:53:03
237	Nadia Bjorlin	person	237	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
238	Steven ?	person	238	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
239	Chori Krove	person	239	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
240	Shannon Healy	person	240	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
241	Melanie Starves	person	241	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
242	Lynn Fontanella	person	242	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
243	Craig Adams	person	243	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
244	Ralph Ellison	person	244	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
245	Gary Roxburgh (Pilot)	person	245	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
246	Henry Rosovsky	person	246	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
247	Adam PerryLang	person	247	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
248	Ron ?	person	248	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
249	Passenger (0)	person	249	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
250	Joe Pagano	person	250	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 3}	0	2026-02-05 22:53:03
251	Larry Summers	person	251	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 25}	0	2026-02-05 22:53:03
252	Luba ?	person	252	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
253	Dara ?	person	253	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
254	Rhonda Sherer	person	254	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
255	Rhonda Sherer's Husband	person	255	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
256	Francois Verenia	person	256	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
257	Shelley Lewis	person	257	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
258	Tiffany Gramza	person	258	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
259	Phillipe Mugnier	person	259	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
260	Inca Doerrig	person	260	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
261	Kirsten ?	person	261	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
262	Charles ?	person	262	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
263	Monica ?	person	263	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
264	Daniel Heller	person	264	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
265	Alexia Wallert	person	265	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
266	Rich ?	person	266	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
267	Glen Dixon	person	267	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
268	Manny Duban	person	268	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
269	Dave Killary	person	269	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
270	Victoria Hazell	person	270	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
271	Marshall ?	person	271	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
726	Erika Kellerhals	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
272	Elizabeth ?	person	272	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
273	Shelly Harrison	person	273	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
274	Audrey Raimbault	person	274	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
275	MR. BROWN	person	275	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
276	Freya Wissing	person	276	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
277	Jean Gathy	person	277	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
278	PBI West Palm Beach, FL, United States	person	278	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
279	36653-G-1159B-N908JE-PBI-TIST-FOIA-1336-No Records ?	person	279	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
280	Christina Estrada	person	280	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
281	Leticia Birkholder	person	281	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
282	Michelle Michelle	person	282	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
283	Bodyguard ?	person	283	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
284	Alexandria ?	person	284	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
285	Peter Marino	person	285	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
286	Frederic Fekkai	person	286	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 24}	0	2026-02-05 22:53:03
287	Alexander Fekkai	person	287	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
288	Audrey Blaise	person	288	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
289	Jasmine ?	person	289	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
290	36738-G-1159B-N908JE-SAF-TEB-FOIA-1371-No Records ?	person	290	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
291	36742-G-1159B-N908JE-TEB-PBI-FOIA-1372-No Records ?	person	291	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
292	36746-G-1159B-N908JE-PBI-TVC-FOIA-1373-No Records ?	person	292	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
293	36747-G-1159B-N908JE-TVC-TEB-FOIA-1374-No Records ?	person	293	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
294	36749-G-1159B-N908JE-TEB-PBI-FOIA-1375-No Records ?	person	294	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
295	36752-G-1159B-N908JE-PBI-TIST-FOIA-1376-No Records ?	person	295	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
296	36757-G-1159B-N908JE-TIST-PBI-FOIA-1377-No Records ?	person	296	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
297	Kelly Spamm	person	297	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
298	Cheri Krape	person	298	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
299	Vor Holding	person	299	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
300	36819-G-1159B-N908JE-LGA-PBI-FOIA-1399-No Records ?	person	300	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
301	Ricardo Legoretta	person	301	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
302	Jessica Bauer	person	302	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
303	Tom Pritzker	person	303	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
304	(MARHAM	person	304	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
305	Cindy Lopez	person	305	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
306	Roger ?	person	306	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
307	TIST West Palm Beach, FL, United States	person	307	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
308	PBI Charlotte Amalie, St. Thomas,	person	308	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
309	36923-G-1159B-N908JE-PBI-SAF-FOIA-1448-No Records ?	person	309	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
310	36926-G-1159B-N908JE-SAF-VNY-FOIA-1449-No Records ?	person	310	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
311	36927-G-1159B-N908JE-VNY-TEB-FOIA-1450-No Records ?	person	311	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
312	36931-G-1159B-N908JE-TEB-BED-FOIA-1451-No Records ?	person	312	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
313	36932-G-1159B-N908JE-BED-PBI-FOIA-1452-No Records ?	person	313	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
314	36933-G-1159B-N908JE-PBI-ABY-FOIA-1453-No Records ?	person	314	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
315	36933-G-1159B-N908JE-ABY-PBI-FOIA-1454-No Records ?	person	315	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
727	Caroline Lang	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
316	36935-G-1159B-N908JE-PBI-TEB-FOIA-1455-No Records ?	person	316	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
317	36938-G-1159B-N908JE-TEB-PBI-FOIA-1456-No Records ?	person	317	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
318	36940-G-1159B-N908JE-PBI-TIST-FOIA-1457-No Records ?	person	318	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
319	36941-G-1159B-N908JE-TIST-PBI-FOIA-1458-No Records ?	person	319	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
320	36944-G-1159B-N908JE-PBI-MRY-FOIA-1459-No Records ?	person	320	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
321	36946-G-1159B-N908JE-MRY-VNY-FOIA-1460-No Records ?	person	321	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
322	36948-G-1159B-N908JE-VNY-SAF-FOIA-1461-No Records ?	person	322	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
323	36949-G-1159B-N908JE-SAF-TEB-FOIA-1462-No Records ?	person	323	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
324	36952-G-1159B-N908JE-TEB-PBI-FOIA-1463-No Records ?	person	324	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
325	LAL Lake City, FL, United States	person	325	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
326	PBI Leesburg, FL, United States	person	326	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
327	PBI Avon Park, FL, United States	person	327	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
328	PBI Key West, FL, United States	person	328	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
329	EYW West Palm Beach, FL, United States	person	329	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
330	PBI Fort Lauderdale, FL, United States	person	330	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
331	Koluk-Koylu, Banu Banu Koluk-	person	331	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
332	Cheri Lynch	person	332	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
333	Ed Tuttle	person	333	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
334	E JUTHLE?	person	334	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
335	FLL Miami, FL, United States	person	335	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
336	Marvin Minsky	person	336	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 10}	0	2026-02-05 22:53:03
337	Henry Jarecki	person	337	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 2}	0	2026-02-05 22:53:03
338	GAI Teterboro, NJ, United States	person	338	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
339	Lydia ?	person	339	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
340	Joann ?	person	340	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
341	Michelle ?	person	341	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
342	Kyle Tayler	person	342	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
343	27K Macon, GA, United States	person	343	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
344	JVY Columbus, OH, United States	person	344	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
345	MCN West Palm Beach, FL, United States	person	345	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
346	27K Jeffersonville, IN, United States	person	346	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
347	GNV Madison, IN, United States	person	347	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
348	TEB Charlotte Amalie, St. Thomas,	person	348	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
349	PBI Orlando, FL, United States	person	349	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
350	PBI Teterboro, NJ, United States	person	350	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
351	LAL West Palm Beach, FL, United States	person	351	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
352	MCN Lakeland, FL, United States	person	352	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
353	ISM Macon, GA, United States	person	353	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
354	TEB West Palm Beach, FL, United States	person	354	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
355	Naomi Campbell	person	355	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 2}	0	2026-02-05 22:53:03
356	Rebecca White	person	356	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
357	Anouk Lavalee	person	357	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
358	Anna Molova	person	358	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
359	David Bolivaras	person	359	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
360	Sheridan Gibson	person	360	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
361	Cristalle Wasche	person	361	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
362	E KATERINA GRINEVA	person	362	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
363	Taylor ?	person	363	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
364	Mike Donovan	person	364	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
365	AMA Jackson, MS, United States	person	365	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
366	ABQ Seattle, WA, United States	person	366	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
367	ZORRO Albuquerque, NM, United States	person	367	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
368	Fleur PerryLang	person	368	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
369	Jonathan Mano (Pilot)	person	369	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
370	Gil ?	person	370	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
371	Gurly ?	person	371	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
372	Robert ?	person	372	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
373	HPN Charlotte Amalie, St. Thomas,	person	373	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
374	Alexandria Dixon	person	374	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
375	Karen Casey	person	375	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
376	Steve ?	person	376	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
377	Bonnie ?	person	377	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
378	Julie Shay	person	378	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
379	ZORRO Santa Fe, NM, United States	person	379	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
380	Mglindallns E?	person	380	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
381	Edwardo ?	person	381	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
382	Geor Tintay?	person	382	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
383	Chauntae Davies	person	383	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
384	Bob Breslen (Pilot)	person	384	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
385	37318-B-727-31-N908JE-PBI-JFK-FOIA-071A-No Records ?	person	385	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
386	37322-B-727-31-N908JE-JFK-TIST-FOIA-072A-No Records ?	person	386	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
387	Brent Tindall (Chef)	person	387	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
388	Susan Hamblin	person	388	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
389	Julie Fierson	person	389	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
390	Fabriame Palheo	person	390	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
391	Andrea Mitrovich	person	391	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
392	MACKLA ?	person	392	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
393	MYLENE ?	person	393	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
394	Catherine Derby	person	394	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
395	Mylene Arm	person	395	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
396	Todd Meistor	person	396	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
397	LGB Long Beach, CA, United States	person	397	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
398	Marcinkova, Nadia Nadia	person	398	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
399	Teala Davies	person	399	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
400	Fran ?	person	400	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
401	Valdson Cotrin	person	401	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 23}	0	2026-02-05 22:53:03
402	MBPV Great Exuma, Bahamas	person	402	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
403	TIST Charlotte Amalie, St. Thomas,	person	403	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
404	Carolina ?	person	404	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
405	Jerry Goldsmith	person	405	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
406	Doug Band	person	406	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
407	Secret Service (4)	person	407	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
408	Ira Magaziner	person	408	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
409	Joe Novich	person	409	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
410	Jantelle Torie	person	410	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
411	Scott Rueber	person	411	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
412	Vick Lambro	person	412	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
413	Chris Camaros	person	413	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
414	Tom Payette	person	414	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
415	?, MORGAN RRY MORGAN RRY ?	person	415	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
416	Michael Durberry (Pilot)	person	416	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
417	Kimberly Burns	person	417	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
418	Brent Tindall	person	418	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
419	Steve Lister (Pilot)	person	419	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
420	Gary Roxbury	person	420	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
421	Manuela Stoetter	person	421	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
422	Larry Visoski	person	422	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 90}	0	2026-02-05 22:53:03
423	Bruce ?	person	423	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
424	Larry Morrison (Pilot)	person	424	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
425	Aline Weber	person	425	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
426	Nina Keita	person	426	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
427	Forest Sawyer	person	427	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
428	Steve Lester	person	428	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
429	Jennifer Kalin	person	429	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
430	Tami ?	person	430	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
431	Devonvoisin, Ariane	person	431	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
432	GOSMAN ?	person	432	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
433	Natalya Malyshov	person	433	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
434	SEMOINE ?	person	434	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
435	FLORA ?	person	435	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
436	ZSUIZSA ?	person	436	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
437	CZI FRIK?	person	437	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
438	Stefanie ?	person	438	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
439	Steve Miller	person	439	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
440	Larry Morrison	person	440	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
441	Jo-Jo Fontanella	person	441	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
442	David Mullen	person	442	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 4}	0	2026-02-05 22:53:03
443	Frank Gamble (Pilot)	person	443	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
444	Kristy Rodgers (Pilot)	person	444	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
445	Patsy Rodgers	person	445	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
446	Ralph Pascale (Pilot)	person	446	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
447	NATALIE ?	person	447	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
448	TIST Water Island, St. Thomas, United	person	448	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
449	PIA TRUSELL (Pilot)	person	449	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
450	Adriana Mucinska	person	450	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
451	Zina Broukis	person	451	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
452	Dana Burns	person	452	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
453	Neil Biggen	person	453	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
454	Pete Rathgeb	person	454	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
455	Colleen ?	person	455	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
456	Cresencia Valdez	person	456	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
457	Bill Hammond (Pilot)	person	457	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
458	Bill Murphy (Pilot)	person	458	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
459	Tatiana Kovylina	person	459	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
460	IAN ?	person	460	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
461	Jim Dowd	person	461	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
462	Alex Resnick	person	462	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
463	Natalie Simanova	person	463	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
464	Mr. Mucinska	person	464	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
465	Mrs. Mucinska	person	465	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
466	Sandy Berger	person	466	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
467	Paula Halada	person	467	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
468	George Goyer	person	468	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
469	Igor Zinoviev	person	469	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 1}	0	2026-02-05 22:53:03
470	Mark Tagoya	person	470	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
471	Juan Molyneux	person	471	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned"}	0	2026-02-05 22:53:03
472	Lisa Summers	person	472	persons	\N	{"notes": "Auto-created from flight logs", "person_type": "mentioned", "ds10_mention_count": 2}	0	2026-02-05 22:53:03
473	Anonymous Victim	person	473	persons	\N	{"notes": "Placeholder for unidentified victims in victim_perpetrator_links", "person_type": "victim"}	0	2026-02-05 22:53:03
474	The 1953 Trust	organization	1	organizations	\N	{"org_type": "foundation", "jurisdiction": "Virgin Islands"}	0	2026-02-05 22:53:03
475	Southern Trust Company, Inc.	shell_company	2	organizations	\N	{"org_type": "shell_company", "jurisdiction": "Virgin Islands"}	0	2026-02-05 22:53:03
476	Financial Trust, Inc.	shell_company	3	organizations	\N	{"org_type": "shell_company", "jurisdiction": "Unknown"}	0	2026-02-05 22:53:03
477	Hyperion Air, LLC	shell_company	4	organizations	\N	{"org_type": "shell_company", "jurisdiction": "Unknown"}	0	2026-02-05 22:53:03
478	JSC Interiors, LLC	shell_company	5	organizations	\N	{"org_type": "shell_company", "jurisdiction": "Unknown"}	0	2026-02-05 22:53:03
479	Plan D, LLC	shell_company	6	organizations	\N	{"org_type": "shell_company", "jurisdiction": "Virgin Islands"}	0	2026-02-05 22:53:03
480	Great St. Jim, LLC	shell_company	7	organizations	\N	{"org_type": "shell_company", "jurisdiction": "Virgin Islands"}	0	2026-02-05 22:53:03
481	Financial Strategy Group, Ltd.	shell_company	\N	\N	\N	{"source": "EVIDENCE_COMPILATION.md", "org_type": "shell_company", "jurisdiction": "Unknown"}	0	2026-02-05 22:53:03
482	Hyperion Air, Inc.	shell_company	\N	\N	\N	{"source": "EVIDENCE_COMPILATION.md", "org_type": "shell_company", "jurisdiction": "Unknown"}	0	2026-02-05 22:53:03
483	Little St. James Island	location	1	locations	\N	{"address": "U.S. Virgin Islands", "location_type": "island", "known_abuse_location": true}	0	2026-02-05 22:53:03
484	9 East 71st Street	property	2	locations	\N	{"address": "New York, NY", "location_type": "residence", "known_abuse_location": true}	0	2026-02-05 22:53:03
485	358 El Brillo Way	property	3	locations	\N	{"address": "Palm Beach, FL", "location_type": "residence", "known_abuse_location": true}	0	2026-02-05 22:53:03
486	Zorro Ranch	property	4	locations	\N	{"address": "Stanley, NM", "location_type": "ranch", "known_abuse_location": true}	0	2026-02-05 22:53:03
487	Great St. James Island	location	5	locations	\N	{"address": "U.S. Virgin Islands", "location_type": "island"}	0	2026-02-05 22:53:03
488	9 East 71st Street, NYC	property	\N	\N	\N	{"source": "EVIDENCE_COMPILATION.md", "address": "New York, NY", "location_type": "residence", "known_abuse_location": true}	0	2026-02-05 22:53:03
489	358 El Brillo Way, Palm Beach	property	\N	\N	\N	{"source": "EVIDENCE_COMPILATION.md", "address": "Palm Beach, FL", "location_type": "residence", "known_abuse_location": true}	0	2026-02-05 22:53:03
490	Little St. James Island, USVI	location	\N	\N	\N	{"source": "EVIDENCE_COMPILATION.md", "address": "U.S. Virgin Islands", "location_type": "island", "known_abuse_location": true}	0	2026-02-05 22:53:03
491	Zorro Ranch, Stanley, NM	property	\N	\N	\N	{"source": "EVIDENCE_COMPILATION.md", "address": "Stanley, NM", "location_type": "ranch", "known_abuse_location": true}	0	2026-02-05 22:53:03
492	Paris apartment, 16th Arrondissement	property	\N	\N	\N	{"source": "EVIDENCE_COMPILATION.md", "address": "Paris, France", "location_type": "residence", "known_abuse_location": false}	0	2026-02-05 22:53:03
493	N908JE (Boeing 727-31)	aircraft	\N	\N	\N	{"owner": "Jeffrey Epstein", "nickname": "Lolita Express", "tail_number": "N908JE", "aircraft_type": "Boeing 727-31"}	0	2026-02-05 22:53:03
494	N909JE (Gulfstream II)	aircraft	\N	\N	\N	{"owner": "Jeffrey Epstein", "tail_number": "N909JE", "aircraft_type": "Gulfstream II/SP"}	0	2026-02-05 22:53:03
495	N212JE (Cessna 421)	aircraft	\N	\N	\N	{"owner": "Jeffrey Epstein", "tail_number": "N212JE", "aircraft_type": "Cessna 421"}	0	2026-02-05 22:53:03
496	N34JE (Helicopter)	aircraft	\N	\N	\N	{"owner": "Jeffrey Epstein", "tail_number": "N34JE", "aircraft_type": "Helicopter"}	0	2026-02-05 22:53:03
497	Deutsche Bank	organization	\N	\N	\N	{"notes": "Financial institution with multiple Epstein accounts", "source": "ds10", "org_type": "bank"}	0	2026-02-06 00:37:41
498	JPMorgan Chase	organization	\N	\N	\N	{"notes": "Financial institution with Epstein accounts", "source": "ds10", "org_type": "bank"}	0	2026-02-06 00:37:41
499	Deutsche Bank Securities Inc.	organization	\N	\N	\N	{"notes": "Securities arm; offered securities through this entity", "source": "ds10", "org_type": "bank"}	0	2026-02-06 00:37:41
728	Reid Hoffman	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
500	Deutsche Bank Trust Co Americas	organization	\N	\N	\N	{"notes": "Trust subsidiary at 60 Wall St", "source": "ds10", "org_type": "bank"}	0	2026-02-06 00:37:41
501	SunTrust	organization	\N	\N	\N	{"notes": "Bank with Epstein-related accounts", "source": "ds10", "org_type": "bank"}	0	2026-02-06 00:37:41
502	The Haze Trust	shell_company	\N	\N	\N	{"notes": "Trust entity found in DS10 financial documents", "source": "ds10", "org_type": "foundation"}	0	2026-02-06 00:37:41
503	Insurance Trust	shell_company	\N	\N	\N	{"notes": "Epstein insurance trust; beneficiaries include Shuliak, Indyke", "source": "ds10", "org_type": "foundation"}	0	2026-02-06 00:37:41
504	Caterpillar Trust 2	shell_company	\N	\N	\N	{"notes": "Trust entity; Indyke/Kahn connected", "source": "ds10", "org_type": "foundation"}	0	2026-02-06 00:37:41
505	GSR Mortgage Loan Trust 2005-5F	shell_company	\N	\N	\N	{"notes": "Mortgage-backed security in Maxwell accounts", "source": "ds10", "org_type": "foundation"}	0	2026-02-06 00:37:41
506	FBI	organization	\N	\N	\N	{"notes": "Federal Bureau of Investigation", "source": "ds10", "org_type": "government"}	0	2026-02-06 00:37:41
507	MCC New York	organization	\N	\N	\N	{"notes": "Metropolitan Correctional Center, New York", "source": "ds10", "org_type": "government"}	0	2026-02-06 00:37:41
508	SDNY	organization	\N	\N	\N	{"notes": "Southern District of New York US Attorney's Office", "source": "ds10", "org_type": "government"}	0	2026-02-06 00:37:41
509	Howard Lutnick	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "CEO Cantor Fitzgerald", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; alleged financial crimes connection; neighboring property transaction", "person_type": "mentioned", "public_figure": true, "ds10_mention_count": 5}	0	2026-02-06 00:37:42
510	William Barr	person	\N	\N	["Barr"]	{"source": "ds10_analysis", "occupation": "Former US Attorney General", "ds10_detail": "Named in FBI PROMINENT NAMES briefing; NTOC tip alleging present during abuses; victim encounter at model event", "person_type": "mentioned", "public_figure": true, "ds10_mention_count": 5}	0	2026-02-06 00:37:42
511	Ehud Barak	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "Former Israeli Prime Minister", "ds10_detail": "Breakfast meeting scheduled with Epstein per calendar (EFTA02154241)", "person_type": "associate", "public_figure": true, "ds10_mention_count": 7}	0	2026-02-06 00:37:43
512	Tom Barrack	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "Investor, Colony Capital founder", "ds10_detail": "Scheduling communication for meetings (EFTA02176329)", "person_type": "mentioned", "public_figure": true, "ds10_mention_count": 4}	0	2026-02-06 00:37:43
513	Bob Shapiro	person	\N	\N	["Robert Shapiro"]	{"source": "ds10_analysis", "occupation": "Attorney", "ds10_detail": "Named in unverified NTOC tip alongside Dershowitz; no contact info provided by tipster", "person_type": "mentioned", "public_figure": true, "ds10_mention_count": 2}	0	2026-02-06 00:37:43
514	Elon Musk	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "CEO Tesla/SpaceX", "ds10_detail": "Named in single unverified NTOC anonymous tip only; no corroboration; FBI could not follow up (no contact info)", "person_type": "mentioned", "public_figure": true, "ds10_mention_count": 6}	0	2026-02-06 00:37:43
515	Andrew Cuomo	person	\N	\N	["Cuomo"]	{"source": "ds10_analysis", "occupation": "Former NY Governor", "ds10_detail": "Mentioned in NTOC tip context and FBI PROMINENT NAMES briefing", "person_type": "mentioned", "public_figure": true, "ds10_mention_count": 2}	0	2026-02-06 00:37:43
516	Simon Andriesz	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "Unknown", "ds10_detail": "Source of allegations about Lutnick in FBI PROMINENT NAMES briefing", "person_type": "mentioned", "ds10_mention_count": 2}	0	2026-02-06 00:37:43
517	Steve Scully	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "Unknown", "ds10_detail": "Witness named in FBI PROMINENT NAMES briefing re: Prince Andrew; noted as having criminal history", "person_type": "mentioned", "ds10_mention_count": 2}	0	2026-02-06 00:37:43
518	Alfredo Rodriguez	person	\N	\N	["Rodriquez"]	{"source": "ds10_analysis", "occupation": "Former Epstein employee", "ds10_detail": "Former Epstein employee; convicted of obstruction; source of black book", "person_type": "mentioned", "ds10_mention_count": 7}	0	2026-02-06 00:37:43
519	Nicholas Tartaglione	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "Inmate", "ds10_detail": "MCC cellmate with Epstein in SHU before first suicide attempt", "person_type": "mentioned", "ds10_mention_count": 0}	0	2026-02-06 00:37:43
520	Efrain Reyes	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "Inmate", "ds10_detail": "MCC cellmate released day before Epstein death; interviewed by AUSA", "person_type": "mentioned", "ds10_mention_count": 1}	0	2026-02-06 00:37:43
521	Michael Thomas	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "MCC Corrections Officer", "ds10_detail": "MCC CO on duty during Epstein death; charged and DPA", "person_type": "mentioned", "ds10_mention_count": 3}	0	2026-02-06 00:37:43
522	Tova Noel	person	\N	\N	\N	{"source": "ds10_analysis", "occupation": "MCC Corrections Officer", "ds10_detail": "MCC CO charged with conspiracy re: Epstein death; DPA", "person_type": "mentioned", "ds10_mention_count": 0}	0	2026-02-06 00:37:44
523	Karyna Shuliak	person	\N	\N	\N	{"source": "ds10_trust_docs", "ds10_mention_count": 112}	0	2026-02-06 00:37:46
524	Kevin Maxwell	person	\N	\N	\N	{"source": "ds10_trust_docs", "ds10_mention_count": 3}	0	2026-02-06 00:37:46
710	Boris Nikolic	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
711	Noam Chomsky	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
712	Deepak Chopra	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
713	Richard Joslin	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
714	Bella Klein	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
715	Emad Hanna	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
716	Peggy Siegal	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
717	Peter Attia	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
718	Andrew Farkas	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
719	Al Seckel	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
720	Brad Karp	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
721	Peter Mandelson	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
722	Cecile de Jongh	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
723	Matthew I. Menchel	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
724	David Mitchell	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
729	Paul Morris	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
730	Nicole Junkermann	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
731	Richard Branson	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
732	Lawrence Krauss	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
733	Peter Thiel	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
734	Nathan Myhrvold	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
735	Greg Wyler	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
736	Brice Gordon	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
737	Jennie Saunders	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
738	Joi Ito	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
739	Reid Weingarten	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
740	Mark Lloyd	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
741	Martin Weinberg	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
742	Steve Bannon	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
743	Bradley Edwards	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
744	Paul Cassell	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
745	Barry Josephson	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
746	Steven Sinofsky	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
747	Austin Hill	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
748	Nicholas Ribis	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
749	Jeanne Brennan Wiebracht	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
750	Mark Tramo	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
751	Mark Epstein	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
752	Dr. Jarecki	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
753	Lisa Randall	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
754	Carluz Toylo	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
755	John Brockman	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
756	Brock Pierce	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
757	Stephen Kosslyn	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
758	David Stern	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
759	Michael Ovitz	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
760	Kimbal Musk	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
761	George Church	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
762	Barnaby Marsh	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
763	Kathryn Ruemmler	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
764	Janusz Banasiak	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
765	Jean Luc Brunel	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
766	Harry Beller	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
767	Michael Wolff	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
768	Martin Nowak	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
769	Bobby Kotick	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
770	Michelle	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
771	Daniel Siad	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
772	Dana	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
773	Tancredi Marchiolo	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
774	Danny Hillis	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
775	Josh Harris	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
776	Tim Zagat	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
777	Jesse	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
778	Arda Beskardes	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
779	Roy Black	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
780	Alexander Acosta	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
781	Jay Lefkowitz	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
782	Wallace Cunningham	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
783	Dick Cavett	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
784	Ben Goertzel	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
785	Stuart Hameroff	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
786	Katie Couric	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
787	Kenneth Starr	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
788	Mary Erdoes	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
789	Harry Fisch	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
790	Robert Trivers	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
791	Nathan Wolfe	person	\N	\N	\N	{"source": "communications_db"}	0	2026-02-18 02:51:29
\.


--
-- Data for Name: relationships; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.relationships (id, source_entity_id, target_entity_id, relationship_type, weight, date_first, date_last, metadata, created_at) FROM stdin;
1	1	2	traveled_with	387	1996-01-01	2006-01-19	{"total_dates": 341, "sample_dates": ["1996-01-01", "1996-01-12", "1996-01-20", "1996-01-21", "1996-01-28", "1996-02-05", "1996-02-07", "1996-02-09", "1996-02-12", "1996-02-28"], "shared_flight_count": 387}	2026-02-05 22:53:03
2	1	6	traveled_with	3	2000-05-12	2004-10-17	{"total_dates": 3, "sample_dates": ["2000-05-12", "2004-10-16", "2004-10-17"], "shared_flight_count": 3}	2026-02-05 22:53:03
3	1	7	traveled_with	9	1996-09-08	2005-11-17	{"total_dates": 8, "sample_dates": ["1996-09-08", "1996-09-09", "1997-01-11", "1998-02-09", "1998-10-21", "1999-04-16", "2004-02-05", "2005-11-17"], "shared_flight_count": 9}	2026-02-05 22:53:03
4	1	8	traveled_with	18	1995-11-21	2004-04-11	{"total_dates": 17, "sample_dates": ["1995-11-21", "1996-04-08", "1996-11-07", "1996-11-17", "1997-02-17", "1997-04-17", "1997-08-20", "1997-10-31", "1997-12-14", "1998-01-03"], "shared_flight_count": 18}	2026-02-05 22:53:03
5	1	9	traveled_with	16	2000-05-08	2005-02-03	{"total_dates": 13, "sample_dates": ["2000-05-08", "2003-07-02", "2004-01-02", "2004-01-05", "2004-01-08", "2004-02-02", "2004-02-12", "2004-02-17", "2004-04-02", "2004-05-12"], "shared_flight_count": 16}	2026-02-05 22:53:03
6	1	10	traveled_with	171	2001-01-06	2006-01-19	{"total_dates": 143, "sample_dates": ["2001-01-06", "2001-10-05", "2001-10-08", "2001-10-11", "2001-10-15", "2001-10-18", "2001-10-23", "2001-10-26", "2001-10-30", "2001-11-03"], "shared_flight_count": 171}	2026-02-05 22:53:03
7	1	13	traveled_with	5	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 5}	2026-02-05 22:53:03
8	1	14	traveled_with	1	1997-01-05	1997-01-05	{"total_dates": 1, "sample_dates": ["1997-01-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
9	1	81	traveled_with	34	1995-11-21	2004-10-10	{"total_dates": 32, "sample_dates": ["1995-11-21", "1996-03-24", "1996-04-08", "1996-05-02", "1996-11-07", "1996-11-11", "1996-11-17", "1996-12-12", "1997-01-05", "1997-02-13"], "shared_flight_count": 34}	2026-02-05 22:53:03
10	1	85	traveled_with	22	2000-12-11	2001-07-28	{"total_dates": 20, "sample_dates": ["2000-12-11", "2000-12-14", "2001-01-26", "2001-03-05", "2001-03-06", "2001-03-08", "2001-03-09", "2001-03-11", "2001-03-27", "2001-04-11"], "shared_flight_count": 22}	2026-02-05 22:53:03
11	1	107	traveled_with	34	1995-11-21	2004-10-10	{"total_dates": 32, "sample_dates": ["1995-11-21", "1996-03-22", "1996-03-24", "1996-04-08", "1996-11-07", "1996-11-11", "1996-11-17", "1996-12-12", "1997-01-05", "1997-02-13"], "shared_flight_count": 34}	2026-02-05 22:53:03
12	1	109	traveled_with	1	1996-04-29	1996-04-29	{"total_dates": 1, "sample_dates": ["1996-04-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
13	1	112	traveled_with	28	1995-11-29	2000-07-19	{"total_dates": 27, "sample_dates": ["1995-11-29", "1995-11-30", "1995-12-03", "1996-01-04", "1996-01-09", "1996-02-28", "1996-03-04", "1996-03-22", "1997-02-13", "1997-02-23"], "shared_flight_count": 28}	2026-02-05 22:53:03
14	1	113	traveled_with	27	1996-01-01	2001-11-30	{"total_dates": 23, "sample_dates": ["1996-01-01", "1996-12-02", "1996-12-04", "1996-12-20", "1996-12-23", "1997-01-29", "1997-01-30", "1997-04-15", "1997-04-17", "1997-12-17"], "shared_flight_count": 27}	2026-02-05 22:53:03
15	1	114	traveled_with	1	1996-01-01	1996-01-01	{"total_dates": 1, "sample_dates": ["1996-01-01"], "shared_flight_count": 1}	2026-02-05 22:53:03
16	1	115	traveled_with	1	1996-01-01	1996-01-01	{"total_dates": 1, "sample_dates": ["1996-01-01"], "shared_flight_count": 1}	2026-02-05 22:53:03
17	1	116	traveled_with	1	1996-01-12	1996-01-12	{"total_dates": 1, "sample_dates": ["1996-01-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
18	1	117	traveled_with	2	1996-02-09	1996-02-12	{"total_dates": 2, "sample_dates": ["1996-02-09", "1996-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
19	1	118	traveled_with	4	1996-12-12	1998-02-12	{"total_dates": 4, "sample_dates": ["1996-12-12", "1997-12-17", "1998-01-03", "1998-02-12"], "shared_flight_count": 4}	2026-02-05 22:53:03
20	1	119	traveled_with	4	1996-12-12	1998-02-12	{"total_dates": 4, "sample_dates": ["1996-12-12", "1997-12-17", "1998-01-03", "1998-02-12"], "shared_flight_count": 4}	2026-02-05 22:53:03
21	1	123	traveled_with	3	1996-08-18	2000-09-29	{"total_dates": 3, "sample_dates": ["1996-08-18", "1996-11-11", "2000-09-29"], "shared_flight_count": 3}	2026-02-05 22:53:03
22	1	124	traveled_with	1	1996-03-04	1996-03-04	{"total_dates": 1, "sample_dates": ["1996-03-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
23	1	125	traveled_with	1	1996-03-08	1996-03-08	{"total_dates": 1, "sample_dates": ["1996-03-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
24	1	126	traveled_with	1	1996-03-11	1996-03-11	{"total_dates": 1, "sample_dates": ["1996-03-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
25	1	127	traveled_with	37	1996-03-18	2000-02-02	{"total_dates": 35, "sample_dates": ["1996-03-18", "1997-01-24", "1997-01-25", "1997-03-08", "1997-03-10", "1997-09-22", "1997-10-17", "1998-02-09", "1998-04-19", "1998-05-09"], "shared_flight_count": 37}	2026-02-05 22:53:03
26	1	128	traveled_with	1	1996-03-22	1996-03-22	{"total_dates": 1, "sample_dates": ["1996-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
27	1	129	traveled_with	3	1996-03-22	1996-11-11	{"total_dates": 3, "sample_dates": ["1996-03-22", "1996-11-07", "1996-11-11"], "shared_flight_count": 3}	2026-02-05 22:53:03
28	1	130	traveled_with	3	1996-03-24	1996-10-30	{"total_dates": 3, "sample_dates": ["1996-03-24", "1996-04-26", "1996-10-30"], "shared_flight_count": 3}	2026-02-05 22:53:03
29	1	131	traveled_with	1	1996-05-02	1996-05-02	{"total_dates": 1, "sample_dates": ["1996-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
30	1	132	traveled_with	1	1996-05-02	1996-05-02	{"total_dates": 1, "sample_dates": ["1996-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
31	1	133	traveled_with	1	1996-05-02	1996-05-02	{"total_dates": 1, "sample_dates": ["1996-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
32	1	134	traveled_with	1	1996-05-02	1996-05-02	{"total_dates": 1, "sample_dates": ["1996-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
33	1	136	traveled_with	4	1996-05-03	1996-05-06	{"total_dates": 2, "sample_dates": ["1996-05-03", "1996-05-06"], "shared_flight_count": 4}	2026-02-05 22:53:03
34	1	137	traveled_with	3	1996-05-08	1996-05-09	{"total_dates": 2, "sample_dates": ["1996-05-08", "1996-05-09"], "shared_flight_count": 3}	2026-02-05 22:53:03
35	1	138	traveled_with	1	1996-05-27	1996-05-27	{"total_dates": 1, "sample_dates": ["1996-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
36	1	139	traveled_with	4	1996-06-02	1997-02-23	{"total_dates": 4, "sample_dates": ["1996-06-02", "1996-06-05", "1997-02-21", "1997-02-23"], "shared_flight_count": 4}	2026-02-05 22:53:03
37	1	140	traveled_with	2	1996-06-02	1996-06-05	{"total_dates": 2, "sample_dates": ["1996-06-02", "1996-06-05"], "shared_flight_count": 2}	2026-02-05 22:53:03
38	1	141	traveled_with	1	1996-06-02	1996-06-02	{"total_dates": 1, "sample_dates": ["1996-06-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
39	1	142	traveled_with	1	1996-06-05	1996-06-05	{"total_dates": 1, "sample_dates": ["1996-06-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
40	1	144	traveled_with	2	1996-07-10	1996-10-15	{"total_dates": 2, "sample_dates": ["1996-07-10", "1996-10-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
41	1	145	traveled_with	1	1996-07-16	1996-07-16	{"total_dates": 1, "sample_dates": ["1996-07-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
42	1	146	traveled_with	1	1996-08-12	1996-08-12	{"total_dates": 1, "sample_dates": ["1996-08-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
43	1	147	traveled_with	5	1996-08-12	1997-10-21	{"total_dates": 5, "sample_dates": ["1996-08-12", "1997-04-15", "1997-04-21", "1997-06-01", "1997-10-21"], "shared_flight_count": 5}	2026-02-05 22:53:03
44	1	148	traveled_with	2	1996-08-12	1999-11-28	{"total_dates": 2, "sample_dates": ["1996-08-12", "1999-11-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
45	1	149	traveled_with	2	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 2}	2026-02-05 22:53:03
46	1	150	traveled_with	3	1996-08-18	1997-04-17	{"total_dates": 2, "sample_dates": ["1996-08-18", "1997-04-17"], "shared_flight_count": 3}	2026-02-05 22:53:03
47	1	151	traveled_with	1	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
48	1	152	traveled_with	18	1996-08-18	1997-11-29	{"total_dates": 15, "sample_dates": ["1996-08-18", "1996-09-12", "1997-01-11", "1997-01-30", "1997-02-02", "1997-02-21", "1997-02-23", "1997-03-15", "1997-04-22", "1997-05-24"], "shared_flight_count": 18}	2026-02-05 22:53:03
49	1	153	traveled_with	6	1996-08-21	1997-02-13	{"total_dates": 5, "sample_dates": ["1996-08-21", "1996-08-26", "1996-12-20", "1996-12-23", "1997-02-13"], "shared_flight_count": 6}	2026-02-05 22:53:03
50	1	154	traveled_with	1	1996-09-08	1996-09-08	{"total_dates": 1, "sample_dates": ["1996-09-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
51	1	155	traveled_with	32	1996-10-06	1997-11-29	{"total_dates": 29, "sample_dates": ["1996-10-06", "1996-10-19", "1996-10-22", "1996-10-31", "1996-11-04", "1996-11-21", "1996-12-04", "1996-12-09", "1997-01-05", "1997-02-25"], "shared_flight_count": 32}	2026-02-05 22:53:03
52	1	156	traveled_with	2	1996-10-15	1996-11-15	{"total_dates": 2, "sample_dates": ["1996-10-15", "1996-11-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
53	1	157	traveled_with	4	1996-10-15	1998-04-09	{"total_dates": 4, "sample_dates": ["1996-10-15", "1996-11-07", "1996-11-11", "1998-04-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
54	1	158	traveled_with	2	1996-10-24	2001-10-15	{"total_dates": 2, "sample_dates": ["1996-10-24", "2001-10-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
55	1	159	traveled_with	1	1996-10-25	1996-10-25	{"total_dates": 1, "sample_dates": ["1996-10-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
56	1	160	traveled_with	10	1996-10-27	2001-11-30	{"total_dates": 10, "sample_dates": ["1996-10-27", "1997-02-02", "1997-03-24", "1998-02-09", "1998-02-12", "2000-01-10", "2000-05-04", "2001-04-17", "2001-11-12", "2001-11-30"], "shared_flight_count": 10}	2026-02-05 22:53:03
57	1	161	traveled_with	1	1996-10-27	1996-10-27	{"total_dates": 1, "sample_dates": ["1996-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
58	1	162	traveled_with	2	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 2}	2026-02-05 22:53:03
59	1	163	traveled_with	2	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 2}	2026-02-05 22:53:03
60	1	164	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
61	1	165	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
62	1	166	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
63	1	167	traveled_with	2	1996-11-07	1996-11-11	{"total_dates": 2, "sample_dates": ["1996-11-07", "1996-11-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
64	1	168	traveled_with	1	1996-11-15	1996-11-15	{"total_dates": 1, "sample_dates": ["1996-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
65	1	169	traveled_with	1	1996-11-15	1996-11-15	{"total_dates": 1, "sample_dates": ["1996-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
66	1	170	traveled_with	1	1996-11-21	1996-11-21	{"total_dates": 1, "sample_dates": ["1996-11-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
67	1	171	traveled_with	1	1996-12-02	1996-12-02	{"total_dates": 1, "sample_dates": ["1996-12-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
68	1	172	traveled_with	1	1996-12-09	1996-12-09	{"total_dates": 1, "sample_dates": ["1996-12-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
2058	496	1	owned_by	1	\N	\N	{"note": "Epstein aircraft", "source": "known_ownership"}	2026-02-05 22:53:03
69	1	173	traveled_with	1	1996-12-09	1996-12-09	{"total_dates": 1, "sample_dates": ["1996-12-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
70	1	174	traveled_with	1	1997-01-11	1997-01-11	{"total_dates": 1, "sample_dates": ["1997-01-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
71	1	175	traveled_with	1	1997-01-21	1997-01-21	{"total_dates": 1, "sample_dates": ["1997-01-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
72	1	176	traveled_with	2	1997-01-24	1997-01-25	{"total_dates": 2, "sample_dates": ["1997-01-24", "1997-01-25"], "shared_flight_count": 2}	2026-02-05 22:53:03
73	1	177	traveled_with	2	1997-01-30	1997-02-02	{"total_dates": 2, "sample_dates": ["1997-01-30", "1997-02-02"], "shared_flight_count": 2}	2026-02-05 22:53:03
74	1	178	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
75	1	179	traveled_with	5	1997-02-17	1998-09-25	{"total_dates": 4, "sample_dates": ["1997-02-17", "1997-06-21", "1997-11-07", "1998-09-25"], "shared_flight_count": 5}	2026-02-05 22:53:03
76	1	180	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
77	1	181	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
78	1	182	traveled_with	2	1997-02-23	1998-02-18	{"total_dates": 2, "sample_dates": ["1997-02-23", "1998-02-18"], "shared_flight_count": 2}	2026-02-05 22:53:03
79	1	183	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
80	1	184	traveled_with	2	1997-02-25	1997-04-10	{"total_dates": 2, "sample_dates": ["1997-02-25", "1997-04-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
81	1	185	traveled_with	1	1997-03-10	1997-03-10	{"total_dates": 1, "sample_dates": ["1997-03-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
82	1	186	traveled_with	1	1997-03-24	1997-03-24	{"total_dates": 1, "sample_dates": ["1997-03-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
83	1	187	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
84	1	188	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
85	1	189	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
86	1	190	traveled_with	3	1997-04-21	2001-09-15	{"total_dates": 3, "sample_dates": ["1997-04-21", "1999-07-25", "2001-09-15"], "shared_flight_count": 3}	2026-02-05 22:53:03
87	1	191	traveled_with	1	1997-05-09	1997-05-09	{"total_dates": 1, "sample_dates": ["1997-05-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
88	1	192	traveled_with	3	1997-05-15	1997-09-26	{"total_dates": 3, "sample_dates": ["1997-05-15", "1997-09-03", "1997-09-26"], "shared_flight_count": 3}	2026-02-05 22:53:03
89	1	193	traveled_with	1	1997-05-24	1997-05-24	{"total_dates": 1, "sample_dates": ["1997-05-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
90	1	194	traveled_with	10	1997-06-21	2001-04-03	{"total_dates": 8, "sample_dates": ["1997-06-21", "1997-06-23", "1997-08-17", "1997-09-01", "1997-09-19", "1997-09-20", "1997-10-12", "2001-04-03"], "shared_flight_count": 10}	2026-02-05 22:53:03
91	1	195	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
92	1	196	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
93	1	197	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
94	1	198	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
95	1	199	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
96	1	200	traveled_with	10	1997-09-26	2001-03-08	{"total_dates": 9, "sample_dates": ["1997-09-26", "1998-05-18", "1998-09-13", "1999-03-31", "1999-04-02", "1999-09-02", "1999-11-11", "1999-11-14", "2001-03-08"], "shared_flight_count": 10}	2026-02-05 22:53:03
97	1	201	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
98	1	202	traveled_with	1	1997-09-28	1997-09-28	{"total_dates": 1, "sample_dates": ["1997-09-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
99	1	203	traveled_with	185	1997-10-17	2001-10-26	{"total_dates": 164, "sample_dates": ["1997-10-17", "1997-10-21", "1997-10-24", "1997-10-27", "1997-10-31", "1997-11-02", "1997-11-04", "1997-11-24", "1997-11-25", "1997-12-06"], "shared_flight_count": 185}	2026-02-05 22:53:03
100	1	204	traveled_with	2	1997-11-04	1998-02-28	{"total_dates": 2, "sample_dates": ["1997-11-04", "1998-02-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
101	1	205	traveled_with	1	1997-11-04	1997-11-04	{"total_dates": 1, "sample_dates": ["1997-11-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
102	1	206	traveled_with	1	1997-11-29	1997-11-29	{"total_dates": 1, "sample_dates": ["1997-11-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
103	1	207	traveled_with	1	1997-11-29	1997-11-29	{"total_dates": 1, "sample_dates": ["1997-11-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
104	1	208	traveled_with	2	1997-12-14	2005-11-16	{"total_dates": 2, "sample_dates": ["1997-12-14", "2005-11-16"], "shared_flight_count": 2}	2026-02-05 22:53:03
105	1	209	traveled_with	10	1997-12-17	1999-11-19	{"total_dates": 9, "sample_dates": ["1997-12-17", "1998-02-09", "1998-03-23", "1998-05-15", "1998-06-04", "1998-09-08", "1999-06-09", "1999-09-13", "1999-11-19"], "shared_flight_count": 10}	2026-02-05 22:53:03
106	1	210	traveled_with	2	1997-12-17	1998-02-12	{"total_dates": 2, "sample_dates": ["1997-12-17", "1998-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
107	1	211	traveled_with	2	1998-01-03	2001-01-11	{"total_dates": 2, "sample_dates": ["1998-01-03", "2001-01-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
108	1	212	traveled_with	2	1998-01-03	2001-01-11	{"total_dates": 2, "sample_dates": ["1998-01-03", "2001-01-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
109	1	213	traveled_with	3	1998-01-08	1998-03-27	{"total_dates": 3, "sample_dates": ["1998-01-08", "1998-01-10", "1998-03-27"], "shared_flight_count": 3}	2026-02-05 22:53:03
110	1	214	traveled_with	4	1998-01-20	1998-05-09	{"total_dates": 3, "sample_dates": ["1998-01-20", "1998-01-25", "1998-05-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
111	1	215	traveled_with	3	1998-01-31	2001-03-22	{"total_dates": 2, "sample_dates": ["1998-01-31", "2001-03-22"], "shared_flight_count": 3}	2026-02-05 22:53:03
112	1	216	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
113	1	217	traveled_with	1	1998-02-18	1998-02-18	{"total_dates": 1, "sample_dates": ["1998-02-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
114	1	218	traveled_with	7	1998-02-28	2004-03-11	{"total_dates": 7, "sample_dates": ["1998-02-28", "2001-04-17", "2001-11-30", "2004-03-07", "2004-03-08", "2004-03-09", "2004-03-11"], "shared_flight_count": 7}	2026-02-05 22:53:03
115	1	220	traveled_with	1	1998-04-05	1998-04-05	{"total_dates": 1, "sample_dates": ["1998-04-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
116	1	221	traveled_with	1	1998-04-05	1998-04-05	{"total_dates": 1, "sample_dates": ["1998-04-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
117	1	222	traveled_with	6	1998-04-05	2000-07-04	{"total_dates": 6, "sample_dates": ["1998-04-05", "1998-06-26", "1998-08-07", "1999-10-18", "2000-01-04", "2000-07-04"], "shared_flight_count": 6}	2026-02-05 22:53:03
118	1	223	traveled_with	1	1998-04-06	1998-04-06	{"total_dates": 1, "sample_dates": ["1998-04-06"], "shared_flight_count": 1}	2026-02-05 22:53:03
119	1	224	traveled_with	2	1998-04-06	1998-04-06	{"total_dates": 1, "sample_dates": ["1998-04-06"], "shared_flight_count": 2}	2026-02-05 22:53:03
120	1	225	traveled_with	3	1998-04-06	2001-06-15	{"total_dates": 3, "sample_dates": ["1998-04-06", "2001-06-13", "2001-06-15"], "shared_flight_count": 3}	2026-02-05 22:53:03
121	1	226	traveled_with	2	1998-04-09	1998-04-09	{"total_dates": 1, "sample_dates": ["1998-04-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
122	1	227	traveled_with	3	1998-04-09	1998-05-05	{"total_dates": 2, "sample_dates": ["1998-04-09", "1998-05-05"], "shared_flight_count": 3}	2026-02-05 22:53:03
123	1	228	traveled_with	1	1998-04-16	1998-04-16	{"total_dates": 1, "sample_dates": ["1998-04-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
124	1	233	traveled_with	2	1998-04-20	1998-04-20	{"total_dates": 1, "sample_dates": ["1998-04-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
125	1	234	traveled_with	2	1998-04-20	1998-04-20	{"total_dates": 1, "sample_dates": ["1998-04-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
126	1	235	traveled_with	1	1998-04-24	1998-04-24	{"total_dates": 1, "sample_dates": ["1998-04-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
127	1	236	traveled_with	7	1998-04-24	2001-03-08	{"total_dates": 6, "sample_dates": ["1998-04-24", "1998-09-13", "1999-03-31", "1999-04-02", "1999-09-02", "2001-03-08"], "shared_flight_count": 7}	2026-02-05 22:53:03
128	1	237	traveled_with	2	1998-05-03	2001-03-31	{"total_dates": 2, "sample_dates": ["1998-05-03", "2001-03-31"], "shared_flight_count": 2}	2026-02-05 22:53:03
129	1	238	traveled_with	1	1998-05-05	1998-05-05	{"total_dates": 1, "sample_dates": ["1998-05-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
130	1	239	traveled_with	2	1998-05-11	1998-05-20	{"total_dates": 2, "sample_dates": ["1998-05-11", "1998-05-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
131	1	240	traveled_with	3	1998-05-18	1999-09-05	{"total_dates": 2, "sample_dates": ["1998-05-18", "1999-09-05"], "shared_flight_count": 3}	2026-02-05 22:53:03
132	1	241	traveled_with	3	1998-06-12	1998-08-04	{"total_dates": 3, "sample_dates": ["1998-06-12", "1998-06-15", "1998-08-04"], "shared_flight_count": 3}	2026-02-05 22:53:03
133	1	242	traveled_with	3	1998-06-18	2004-08-10	{"total_dates": 3, "sample_dates": ["1998-06-18", "1998-06-21", "2004-08-10"], "shared_flight_count": 3}	2026-02-05 22:53:03
134	1	243	traveled_with	1	1998-06-18	1998-06-18	{"total_dates": 1, "sample_dates": ["1998-06-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
135	1	244	traveled_with	1	1998-06-21	1998-06-21	{"total_dates": 1, "sample_dates": ["1998-06-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
136	1	245	traveled_with	30	1998-06-21	2004-08-06	{"total_dates": 23, "sample_dates": ["1998-06-21", "1998-06-23", "1998-06-26", "1999-11-09", "1999-11-11", "1999-11-13", "1999-11-14", "1999-11-16", "2000-07-19", "2000-10-21"], "shared_flight_count": 30}	2026-02-05 22:53:03
137	1	246	traveled_with	1	1998-06-23	1998-06-23	{"total_dates": 1, "sample_dates": ["1998-06-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
138	1	247	traveled_with	13	1998-08-03	2001-08-19	{"total_dates": 12, "sample_dates": ["1998-08-03", "1998-08-21", "1998-10-09", "1998-10-12", "1998-11-20", "1999-05-27", "1999-08-23", "1999-08-26", "1999-09-02", "1999-09-07"], "shared_flight_count": 13}	2026-02-05 22:53:03
139	1	248	traveled_with	1	1998-08-03	1998-08-03	{"total_dates": 1, "sample_dates": ["1998-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
140	1	250	traveled_with	3	1998-08-25	2001-03-22	{"total_dates": 3, "sample_dates": ["1998-08-25", "2000-09-21", "2001-03-22"], "shared_flight_count": 3}	2026-02-05 22:53:03
141	1	251	traveled_with	3	1998-09-19	2005-09-14	{"total_dates": 3, "sample_dates": ["1998-09-19", "2004-04-15", "2005-09-14"], "shared_flight_count": 3}	2026-02-05 22:53:03
142	1	252	traveled_with	1	1998-10-04	1998-10-04	{"total_dates": 1, "sample_dates": ["1998-10-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
143	1	253	traveled_with	1	1998-10-04	1998-10-04	{"total_dates": 1, "sample_dates": ["1998-10-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
144	1	254	traveled_with	3	1998-10-06	2001-04-04	{"total_dates": 2, "sample_dates": ["1998-10-06", "2001-04-04"], "shared_flight_count": 3}	2026-02-05 22:53:03
145	1	255	traveled_with	1	1998-10-06	1998-10-06	{"total_dates": 1, "sample_dates": ["1998-10-06"], "shared_flight_count": 1}	2026-02-05 22:53:03
146	1	256	traveled_with	8	1998-11-14	2000-02-02	{"total_dates": 7, "sample_dates": ["1998-11-14", "1998-11-15", "1998-11-16", "1999-03-31", "1999-04-02", "2000-01-31", "2000-02-02"], "shared_flight_count": 8}	2026-02-05 22:53:03
147	1	257	traveled_with	32	1999-05-02	2001-12-15	{"total_dates": 26, "sample_dates": ["1999-05-02", "1999-06-27", "1999-07-29", "1999-09-02", "1999-09-05", "1999-10-07", "1999-10-09", "1999-11-05", "2000-01-16", "2000-05-16"], "shared_flight_count": 32}	2026-02-05 22:53:03
148	1	258	traveled_with	18	1999-04-25	2000-09-26	{"total_dates": 17, "sample_dates": ["1999-04-25", "1999-05-02", "1999-05-10", "1999-05-18", "1999-05-23", "1999-06-04", "1999-06-07", "1999-06-09", "1999-06-15", "1999-07-01"], "shared_flight_count": 18}	2026-02-05 22:53:03
149	1	259	traveled_with	2	1999-03-31	1999-04-02	{"total_dates": 2, "sample_dates": ["1999-03-31", "1999-04-02"], "shared_flight_count": 2}	2026-02-05 22:53:03
150	1	260	traveled_with	5	1999-04-08	2001-05-07	{"total_dates": 4, "sample_dates": ["1999-04-08", "1999-04-11", "1999-05-10", "2001-05-07"], "shared_flight_count": 5}	2026-02-05 22:53:03
151	1	261	traveled_with	1	1999-04-08	1999-04-08	{"total_dates": 1, "sample_dates": ["1999-04-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
152	1	262	traveled_with	1	1999-04-11	1999-04-11	{"total_dates": 1, "sample_dates": ["1999-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
153	1	263	traveled_with	1	1999-04-11	1999-04-11	{"total_dates": 1, "sample_dates": ["1999-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
154	1	264	traveled_with	1	1999-04-25	1999-04-25	{"total_dates": 1, "sample_dates": ["1999-04-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
155	1	265	traveled_with	11	1999-04-25	2001-10-23	{"total_dates": 8, "sample_dates": ["1999-04-25", "2000-05-12", "2001-01-06", "2001-03-15", "2001-03-16", "2001-03-19", "2001-03-22", "2001-10-23"], "shared_flight_count": 11}	2026-02-05 22:53:03
156	1	267	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
157	1	268	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
158	1	269	traveled_with	2	1999-08-07	1999-08-08	{"total_dates": 2, "sample_dates": ["1999-08-07", "1999-08-08"], "shared_flight_count": 2}	2026-02-05 22:53:03
159	1	270	traveled_with	3	1999-09-02	1999-11-30	{"total_dates": 3, "sample_dates": ["1999-09-02", "1999-09-07", "1999-11-30"], "shared_flight_count": 3}	2026-02-05 22:53:03
160	1	271	traveled_with	1	1999-09-08	1999-09-08	{"total_dates": 1, "sample_dates": ["1999-09-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
161	1	272	traveled_with	1	1999-09-09	1999-09-09	{"total_dates": 1, "sample_dates": ["1999-09-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
162	1	273	traveled_with	3	1999-09-25	2000-01-12	{"total_dates": 3, "sample_dates": ["1999-09-25", "1999-09-26", "2000-01-12"], "shared_flight_count": 3}	2026-02-05 22:53:03
163	1	274	traveled_with	4	1999-10-14	1999-10-18	{"total_dates": 3, "sample_dates": ["1999-10-14", "1999-10-16", "1999-10-18"], "shared_flight_count": 4}	2026-02-05 22:53:03
164	1	275	traveled_with	1	1999-10-27	1999-10-27	{"total_dates": 1, "sample_dates": ["1999-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
165	1	276	traveled_with	1	1999-10-27	1999-10-27	{"total_dates": 1, "sample_dates": ["1999-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
166	1	277	traveled_with	2	1999-11-19	1999-11-22	{"total_dates": 2, "sample_dates": ["1999-11-19", "1999-11-22"], "shared_flight_count": 2}	2026-02-05 22:53:03
167	1	280	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
168	1	281	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
169	1	282	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
170	1	283	traveled_with	1	2000-05-12	2000-05-12	{"total_dates": 1, "sample_dates": ["2000-05-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
171	1	284	traveled_with	1	2000-05-15	2000-05-15	{"total_dates": 1, "sample_dates": ["2000-05-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
172	1	285	traveled_with	3	2000-06-25	2000-09-30	{"total_dates": 3, "sample_dates": ["2000-06-25", "2000-09-29", "2000-09-30"], "shared_flight_count": 3}	2026-02-05 22:53:03
173	1	289	traveled_with	1	2000-07-19	2000-07-19	{"total_dates": 1, "sample_dates": ["2000-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
174	1	297	traveled_with	9	2000-08-24	2000-12-09	{"total_dates": 7, "sample_dates": ["2000-08-24", "2000-09-25", "2000-10-21", "2000-12-05", "2000-12-06", "2000-12-07", "2000-12-09"], "shared_flight_count": 9}	2026-02-05 22:53:03
175	1	298	traveled_with	2	2000-09-10	2000-09-12	{"total_dates": 2, "sample_dates": ["2000-09-10", "2000-09-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
176	1	299	traveled_with	1	2000-10-13	2000-10-13	{"total_dates": 1, "sample_dates": ["2000-10-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
177	1	301	traveled_with	3	2000-10-21	2001-03-08	{"total_dates": 3, "sample_dates": ["2000-10-21", "2000-12-01", "2001-03-08"], "shared_flight_count": 3}	2026-02-05 22:53:03
178	1	302	traveled_with	2	2000-11-05	2000-11-07	{"total_dates": 2, "sample_dates": ["2000-11-05", "2000-11-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
179	1	303	traveled_with	1	2000-12-07	2000-12-07	{"total_dates": 1, "sample_dates": ["2000-12-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
180	1	304	traveled_with	1	2000-12-07	2000-12-07	{"total_dates": 1, "sample_dates": ["2000-12-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
181	1	305	traveled_with	4	2001-01-06	2003-08-10	{"total_dates": 4, "sample_dates": ["2001-01-06", "2001-03-16", "2001-03-19", "2003-08-10"], "shared_flight_count": 4}	2026-02-05 22:53:03
182	1	306	traveled_with	12	2001-01-11	2001-03-27	{"total_dates": 9, "sample_dates": ["2001-01-11", "2001-03-08", "2001-03-09", "2001-03-11", "2001-03-15", "2001-03-16", "2001-03-19", "2001-03-22", "2001-03-27"], "shared_flight_count": 12}	2026-02-05 22:53:03
183	1	331	traveled_with	24	2001-03-15	2001-09-09	{"total_dates": 20, "sample_dates": ["2001-03-15", "2001-03-16", "2001-03-19", "2001-03-27", "2001-03-29", "2001-04-05", "2001-04-09", "2001-04-11", "2001-04-16", "2001-04-17"], "shared_flight_count": 24}	2026-02-05 22:53:03
184	1	332	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
185	1	333	traveled_with	5	2001-03-16	2001-09-25	{"total_dates": 3, "sample_dates": ["2001-03-16", "2001-06-28", "2001-09-25"], "shared_flight_count": 5}	2026-02-05 22:53:03
186	1	334	traveled_with	1	2001-03-19	2001-03-19	{"total_dates": 1, "sample_dates": ["2001-03-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
187	1	336	traveled_with	2	2001-03-29	2001-03-31	{"total_dates": 2, "sample_dates": ["2001-03-29", "2001-03-31"], "shared_flight_count": 2}	2026-02-05 22:53:03
188	1	337	traveled_with	3	2001-03-29	2001-04-23	{"total_dates": 3, "sample_dates": ["2001-03-29", "2001-03-31", "2001-04-23"], "shared_flight_count": 3}	2026-02-05 22:53:03
189	1	339	traveled_with	1	2001-04-03	2001-04-03	{"total_dates": 1, "sample_dates": ["2001-04-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
190	1	340	traveled_with	3	2001-04-09	2001-04-11	{"total_dates": 2, "sample_dates": ["2001-04-09", "2001-04-11"], "shared_flight_count": 3}	2026-02-05 22:53:03
191	1	341	traveled_with	1	2001-04-17	2001-04-17	{"total_dates": 1, "sample_dates": ["2001-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
192	1	342	traveled_with	2	2001-04-23	2001-04-23	{"total_dates": 1, "sample_dates": ["2001-04-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
193	1	355	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
194	1	356	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
195	1	357	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
196	1	358	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
197	1	359	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
198	1	360	traveled_with	4	2001-06-15	2001-10-26	{"total_dates": 4, "sample_dates": ["2001-06-15", "2001-07-08", "2001-10-23", "2001-10-26"], "shared_flight_count": 4}	2026-02-05 22:53:03
199	1	361	traveled_with	3	2001-06-22	2005-11-08	{"total_dates": 3, "sample_dates": ["2001-06-22", "2001-12-13", "2005-11-08"], "shared_flight_count": 3}	2026-02-05 22:53:03
200	1	362	traveled_with	1	2001-06-22	2001-06-22	{"total_dates": 1, "sample_dates": ["2001-06-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
201	1	368	traveled_with	4	2001-08-16	2001-12-26	{"total_dates": 3, "sample_dates": ["2001-08-16", "2001-08-19", "2001-12-26"], "shared_flight_count": 4}	2026-02-05 22:53:03
202	1	369	traveled_with	1	2001-08-16	2001-08-16	{"total_dates": 1, "sample_dates": ["2001-08-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
203	1	370	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
204	1	371	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
205	1	372	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
206	1	375	traveled_with	2	2001-09-15	2001-11-30	{"total_dates": 2, "sample_dates": ["2001-09-15", "2001-11-30"], "shared_flight_count": 2}	2026-02-05 22:53:03
207	1	376	traveled_with	1	2001-10-15	2001-10-15	{"total_dates": 1, "sample_dates": ["2001-10-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
208	1	377	traveled_with	2	2001-10-17	2001-10-17	{"total_dates": 1, "sample_dates": ["2001-10-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
209	1	378	traveled_with	5	2001-10-30	2001-11-12	{"total_dates": 3, "sample_dates": ["2001-10-30", "2001-11-09", "2001-11-12"], "shared_flight_count": 5}	2026-02-05 22:53:03
210	1	380	traveled_with	1	2001-11-15	2001-11-15	{"total_dates": 1, "sample_dates": ["2001-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
211	1	381	traveled_with	2	2001-11-23	2001-11-23	{"total_dates": 1, "sample_dates": ["2001-11-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
212	1	382	traveled_with	1	2001-12-13	2001-12-13	{"total_dates": 1, "sample_dates": ["2001-12-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
213	1	383	traveled_with	2	2001-12-13	2004-01-23	{"total_dates": 2, "sample_dates": ["2001-12-13", "2004-01-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
214	1	384	traveled_with	2	2001-12-26	2001-12-26	{"total_dates": 1, "sample_dates": ["2001-12-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
215	1	387	traveled_with	35	2003-06-29	2004-07-22	{"total_dates": 34, "sample_dates": ["2003-06-29", "2003-07-02", "2003-07-07", "2003-07-14", "2003-07-31", "2003-08-10", "2003-08-13", "2003-08-31", "2003-09-22", "2003-10-11"], "shared_flight_count": 35}	2026-02-05 22:53:03
216	1	388	traveled_with	11	2003-06-29	2004-12-03	{"total_dates": 11, "sample_dates": ["2003-06-29", "2003-07-02", "2003-07-07", "2003-07-11", "2003-07-14", "2003-08-31", "2003-09-22", "2003-10-07", "2004-11-23", "2004-11-28"], "shared_flight_count": 11}	2026-02-05 22:53:03
217	1	389	traveled_with	1	2003-06-29	2003-06-29	{"total_dates": 1, "sample_dates": ["2003-06-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
218	1	390	traveled_with	2	2003-07-02	2003-07-07	{"total_dates": 2, "sample_dates": ["2003-07-02", "2003-07-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
219	1	391	traveled_with	27	2003-07-11	2005-11-08	{"total_dates": 20, "sample_dates": ["2003-07-11", "2003-07-14", "2003-07-31", "2003-08-10", "2003-08-13", "2003-09-30", "2003-10-01", "2003-11-04", "2003-11-05", "2003-11-06"], "shared_flight_count": 27}	2026-02-05 22:53:03
220	1	392	traveled_with	1	2003-07-14	2003-07-14	{"total_dates": 1, "sample_dates": ["2003-07-14"], "shared_flight_count": 1}	2026-02-05 22:53:03
221	1	393	traveled_with	1	2003-07-31	2003-07-31	{"total_dates": 1, "sample_dates": ["2003-07-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
222	1	394	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
223	1	395	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
224	1	396	traveled_with	1	2003-08-22	2003-08-22	{"total_dates": 1, "sample_dates": ["2003-08-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
225	1	398	traveled_with	124	2003-09-22	2006-01-19	{"total_dates": 108, "sample_dates": ["2003-09-22", "2003-10-03", "2003-10-06", "2003-12-07", "2004-01-02", "2004-01-03", "2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23"], "shared_flight_count": 124}	2026-02-05 22:53:03
226	1	399	traveled_with	48	2003-09-22	2004-11-14	{"total_dates": 44, "sample_dates": ["2003-09-22", "2003-10-01", "2003-10-03", "2003-10-06", "2003-10-11", "2003-10-26", "2003-12-09", "2003-12-15", "2004-01-12", "2004-01-16"], "shared_flight_count": 48}	2026-02-05 22:53:03
227	1	400	traveled_with	1	2003-09-30	2003-09-30	{"total_dates": 1, "sample_dates": ["2003-09-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
228	1	401	traveled_with	9	2003-10-01	2005-11-12	{"total_dates": 8, "sample_dates": ["2003-10-01", "2004-03-03", "2004-03-11", "2004-03-13", "2004-03-19", "2004-11-14", "2005-04-29", "2005-11-12"], "shared_flight_count": 9}	2026-02-05 22:53:03
229	1	404	traveled_with	1	2003-10-11	2003-10-11	{"total_dates": 1, "sample_dates": ["2003-10-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
230	1	405	traveled_with	1	2003-10-19	2003-10-19	{"total_dates": 1, "sample_dates": ["2003-10-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
231	1	406	traveled_with	5	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 5}	2026-02-05 22:53:03
232	1	407	traveled_with	4	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
233	1	408	traveled_with	2	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
234	1	409	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
235	1	410	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
236	1	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
237	1	412	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
238	1	413	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
239	1	414	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
240	1	416	traveled_with	2	2003-12-07	2003-12-07	{"total_dates": 1, "sample_dates": ["2003-12-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
241	1	417	traveled_with	1	2003-12-15	2003-12-15	{"total_dates": 1, "sample_dates": ["2003-12-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
242	1	418	traveled_with	9	2003-12-24	2004-07-19	{"total_dates": 9, "sample_dates": ["2003-12-24", "2003-12-26", "2004-01-02", "2004-01-05", "2004-01-08", "2004-01-12", "2004-02-09", "2004-07-15", "2004-07-19"], "shared_flight_count": 9}	2026-02-05 22:53:03
243	1	419	traveled_with	1	2003-12-24	2003-12-24	{"total_dates": 1, "sample_dates": ["2003-12-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
244	1	420	traveled_with	1	2003-12-26	2003-12-26	{"total_dates": 1, "sample_dates": ["2003-12-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
245	1	421	traveled_with	1	2004-01-02	2004-01-02	{"total_dates": 1, "sample_dates": ["2004-01-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
246	1	422	traveled_with	126	2004-01-02	2006-01-16	{"total_dates": 109, "sample_dates": ["2004-01-02", "2004-01-03", "2004-01-05", "2004-01-08", "2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23", "2004-01-26", "2004-01-28"], "shared_flight_count": 126}	2026-02-05 22:53:03
247	1	423	traveled_with	2	2004-01-03	2004-01-03	{"total_dates": 1, "sample_dates": ["2004-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
248	1	424	traveled_with	77	2004-01-12	2005-11-28	{"total_dates": 72, "sample_dates": ["2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23", "2004-02-09", "2004-02-12", "2004-02-17", "2004-02-19", "2004-02-22", "2004-02-24"], "shared_flight_count": 77}	2026-02-05 22:53:03
249	1	425	traveled_with	5	2004-02-02	2004-02-22	{"total_dates": 4, "sample_dates": ["2004-02-02", "2004-02-12", "2004-02-17", "2004-02-22"], "shared_flight_count": 5}	2026-02-05 22:53:03
250	1	426	traveled_with	1	2004-02-12	2004-02-12	{"total_dates": 1, "sample_dates": ["2004-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
251	1	427	traveled_with	1	2004-02-24	2004-02-24	{"total_dates": 1, "sample_dates": ["2004-02-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
252	1	428	traveled_with	2	2004-03-13	2004-12-21	{"total_dates": 2, "sample_dates": ["2004-03-13", "2004-12-21"], "shared_flight_count": 2}	2026-02-05 22:53:03
253	1	429	traveled_with	8	2004-04-19	2004-09-16	{"total_dates": 8, "sample_dates": ["2004-04-19", "2004-06-20", "2004-08-06", "2004-08-13", "2004-08-18", "2004-08-19", "2004-09-05", "2004-09-16"], "shared_flight_count": 8}	2026-02-05 22:53:03
254	1	430	traveled_with	1	2004-04-22	2004-04-22	{"total_dates": 1, "sample_dates": ["2004-04-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
255	1	431	traveled_with	1	2004-05-05	2004-05-05	{"total_dates": 1, "sample_dates": ["2004-05-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
256	1	432	traveled_with	1	2004-06-13	2004-06-13	{"total_dates": 1, "sample_dates": ["2004-06-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
257	1	433	traveled_with	4	2004-06-20	2004-09-05	{"total_dates": 4, "sample_dates": ["2004-06-20", "2004-08-06", "2004-08-10", "2004-09-05"], "shared_flight_count": 4}	2026-02-05 22:53:03
258	1	434	traveled_with	4	2004-07-02	2004-07-04	{"total_dates": 2, "sample_dates": ["2004-07-02", "2004-07-04"], "shared_flight_count": 4}	2026-02-05 22:53:03
259	1	435	traveled_with	5	2004-07-02	2004-08-13	{"total_dates": 3, "sample_dates": ["2004-07-02", "2004-07-04", "2004-08-13"], "shared_flight_count": 5}	2026-02-05 22:53:03
260	1	436	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
261	1	437	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
262	1	438	traveled_with	1	2004-07-19	2004-07-19	{"total_dates": 1, "sample_dates": ["2004-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
263	1	439	traveled_with	1	2004-07-22	2004-07-22	{"total_dates": 1, "sample_dates": ["2004-07-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
264	1	440	traveled_with	1	2004-08-03	2004-08-03	{"total_dates": 1, "sample_dates": ["2004-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
265	1	441	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
266	1	442	traveled_with	23	2004-08-10	2005-08-26	{"total_dates": 20, "sample_dates": ["2004-08-10", "2004-08-13", "2004-09-16", "2004-10-20", "2004-10-25", "2004-11-18", "2004-11-23", "2004-11-28", "2005-01-01", "2005-01-03"], "shared_flight_count": 23}	2026-02-05 22:53:03
267	1	443	traveled_with	1	2004-08-19	2004-08-19	{"total_dates": 1, "sample_dates": ["2004-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
268	1	446	traveled_with	1	2004-09-05	2004-09-05	{"total_dates": 1, "sample_dates": ["2004-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
269	1	447	traveled_with	1	2004-10-29	2004-10-29	{"total_dates": 1, "sample_dates": ["2004-10-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
270	1	449	traveled_with	2	2004-11-09	2004-11-10	{"total_dates": 2, "sample_dates": ["2004-11-09", "2004-11-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
271	1	450	traveled_with	12	2004-12-03	2005-11-12	{"total_dates": 12, "sample_dates": ["2004-12-03", "2005-03-01", "2005-04-06", "2005-04-29", "2005-05-12", "2005-05-16", "2005-05-24", "2005-06-01", "2005-07-05", "2005-07-10"], "shared_flight_count": 12}	2026-02-05 22:53:03
272	1	451	traveled_with	2	2005-01-01	2005-01-01	{"total_dates": 1, "sample_dates": ["2005-01-01"], "shared_flight_count": 2}	2026-02-05 22:53:03
273	1	452	traveled_with	8	2005-01-06	2005-04-06	{"total_dates": 8, "sample_dates": ["2005-01-06", "2005-01-31", "2005-02-03", "2005-03-01", "2005-03-24", "2005-03-29", "2005-03-31", "2005-04-06"], "shared_flight_count": 8}	2026-02-05 22:53:03
274	1	457	traveled_with	21	2005-03-24	2005-11-30	{"total_dates": 19, "sample_dates": ["2005-03-24", "2005-03-29", "2005-05-12", "2005-05-16", "2005-05-19", "2005-07-10", "2005-07-22", "2005-07-25", "2005-07-28", "2005-08-01"], "shared_flight_count": 21}	2026-02-05 22:53:03
275	1	459	traveled_with	11	2005-04-29	2005-11-28	{"total_dates": 9, "sample_dates": ["2005-04-29", "2005-07-22", "2005-07-25", "2005-08-02", "2005-09-24", "2005-11-02", "2005-11-17", "2005-11-20", "2005-11-28"], "shared_flight_count": 11}	2026-02-05 22:53:03
276	1	461	traveled_with	1	2005-09-20	2005-09-20	{"total_dates": 1, "sample_dates": ["2005-09-20"], "shared_flight_count": 1}	2026-02-05 22:53:03
277	1	462	traveled_with	2	2005-08-02	2005-09-24	{"total_dates": 2, "sample_dates": ["2005-08-02", "2005-09-24"], "shared_flight_count": 2}	2026-02-05 22:53:03
278	1	463	traveled_with	1	2005-08-02	2005-08-02	{"total_dates": 1, "sample_dates": ["2005-08-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
279	1	464	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
280	1	465	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
281	1	466	traveled_with	1	2005-09-24	2005-09-24	{"total_dates": 1, "sample_dates": ["2005-09-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
282	1	467	traveled_with	1	2005-09-25	2005-09-25	{"total_dates": 1, "sample_dates": ["2005-09-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
283	1	469	traveled_with	4	2005-11-08	2006-01-19	{"total_dates": 4, "sample_dates": ["2005-11-08", "2005-11-12", "2005-11-28", "2006-01-19"], "shared_flight_count": 4}	2026-02-05 22:53:03
284	1	470	traveled_with	2	2005-11-12	2005-11-28	{"total_dates": 2, "sample_dates": ["2005-11-12", "2005-11-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
285	1	471	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
286	2	6	traveled_with	2	2000-05-12	2004-10-17	{"total_dates": 2, "sample_dates": ["2000-05-12", "2004-10-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
287	2	7	traveled_with	1	1998-02-09	1998-02-09	{"total_dates": 1, "sample_dates": ["1998-02-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
288	2	8	traveled_with	15	1995-11-26	2004-04-11	{"total_dates": 14, "sample_dates": ["1995-11-26", "1996-04-08", "1996-11-17", "1997-02-17", "1997-04-17", "1997-10-31", "1998-01-03", "1998-02-06", "1998-04-09", "1998-05-01"], "shared_flight_count": 15}	2026-02-05 22:53:03
289	2	9	traveled_with	6	2000-05-08	2004-05-12	{"total_dates": 5, "sample_dates": ["2000-05-08", "2004-01-02", "2004-02-12", "2004-02-17", "2004-05-12"], "shared_flight_count": 6}	2026-02-05 22:53:03
290	2	10	traveled_with	47	2001-01-06	2006-01-19	{"total_dates": 40, "sample_dates": ["2001-01-06", "2001-09-03", "2001-10-05", "2001-10-08", "2001-10-15", "2001-10-18", "2001-10-23", "2001-11-03", "2001-11-05", "2001-11-15"], "shared_flight_count": 47}	2026-02-05 22:53:03
291	2	13	traveled_with	4	2003-11-05	2003-11-09	{"total_dates": 3, "sample_dates": ["2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
292	2	14	traveled_with	1	1997-01-05	1997-01-05	{"total_dates": 1, "sample_dates": ["1997-01-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
293	2	81	traveled_with	23	1995-11-26	2005-02-19	{"total_dates": 21, "sample_dates": ["1995-11-26", "1996-04-08", "1996-11-17", "1997-01-05", "1997-02-13", "1997-02-17", "1997-04-17", "1997-10-31", "1998-02-06", "1998-03-23"], "shared_flight_count": 23}	2026-02-05 22:53:03
294	2	85	traveled_with	17	2000-12-11	2001-07-16	{"total_dates": 15, "sample_dates": ["2000-12-11", "2000-12-14", "2001-01-26", "2001-03-05", "2001-03-06", "2001-03-08", "2001-03-09", "2001-03-11", "2001-03-27", "2001-04-11"], "shared_flight_count": 17}	2026-02-05 22:53:03
295	2	107	traveled_with	23	1995-11-26	2005-02-19	{"total_dates": 21, "sample_dates": ["1995-11-26", "1996-04-08", "1996-11-17", "1997-01-05", "1997-02-13", "1997-02-17", "1997-04-17", "1997-10-31", "1998-01-03", "1998-02-06"], "shared_flight_count": 23}	2026-02-05 22:53:03
296	2	109	traveled_with	2	1995-11-26	1996-04-29	{"total_dates": 2, "sample_dates": ["1995-11-26", "1996-04-29"], "shared_flight_count": 2}	2026-02-05 22:53:03
297	2	110	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
298	2	111	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
299	2	112	traveled_with	8	1996-02-28	2000-07-19	{"total_dates": 8, "sample_dates": ["1996-02-28", "1996-03-04", "1997-02-13", "1997-05-15", "1998-02-06", "2000-06-30", "2000-07-04", "2000-07-19"], "shared_flight_count": 8}	2026-02-05 22:53:03
300	2	113	traveled_with	14	1996-01-01	2001-04-16	{"total_dates": 14, "sample_dates": ["1996-01-01", "1996-12-02", "1996-12-20", "1996-12-23", "1997-01-29", "1997-04-15", "1997-04-17", "1998-01-20", "1998-01-25", "1998-05-03"], "shared_flight_count": 14}	2026-02-05 22:53:03
301	2	114	traveled_with	1	1996-01-01	1996-01-01	{"total_dates": 1, "sample_dates": ["1996-01-01"], "shared_flight_count": 1}	2026-02-05 22:53:03
302	2	115	traveled_with	1	1996-01-01	1996-01-01	{"total_dates": 1, "sample_dates": ["1996-01-01"], "shared_flight_count": 1}	2026-02-05 22:53:03
303	2	116	traveled_with	1	1996-01-12	1996-01-12	{"total_dates": 1, "sample_dates": ["1996-01-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
304	2	117	traveled_with	2	1996-02-09	1996-02-12	{"total_dates": 2, "sample_dates": ["1996-02-09", "1996-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
305	2	118	traveled_with	2	1998-01-03	1998-02-12	{"total_dates": 2, "sample_dates": ["1998-01-03", "1998-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
306	2	119	traveled_with	2	1998-01-03	1998-02-12	{"total_dates": 2, "sample_dates": ["1998-01-03", "1998-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
307	2	124	traveled_with	1	1996-03-04	1996-03-04	{"total_dates": 1, "sample_dates": ["1996-03-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
308	2	125	traveled_with	1	1996-03-08	1996-03-08	{"total_dates": 1, "sample_dates": ["1996-03-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
309	2	126	traveled_with	1	1996-03-11	1996-03-11	{"total_dates": 1, "sample_dates": ["1996-03-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
310	2	127	traveled_with	30	1996-03-18	2000-02-02	{"total_dates": 27, "sample_dates": ["1996-03-18", "1997-01-24", "1997-01-25", "1997-03-08", "1997-03-10", "1997-09-22", "1997-10-17", "1998-02-09", "1998-05-11", "1998-05-20"], "shared_flight_count": 30}	2026-02-05 22:53:03
311	2	130	traveled_with	1	1996-04-26	1996-04-26	{"total_dates": 1, "sample_dates": ["1996-04-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
312	2	137	traveled_with	3	1996-05-08	1996-05-09	{"total_dates": 2, "sample_dates": ["1996-05-08", "1996-05-09"], "shared_flight_count": 3}	2026-02-05 22:53:03
313	2	138	traveled_with	1	1996-05-27	1996-05-27	{"total_dates": 1, "sample_dates": ["1996-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
314	2	144	traveled_with	1	1996-07-10	1996-07-10	{"total_dates": 1, "sample_dates": ["1996-07-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
315	2	146	traveled_with	1	1996-08-12	1996-08-12	{"total_dates": 1, "sample_dates": ["1996-08-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
316	2	147	traveled_with	3	1996-08-12	1997-10-21	{"total_dates": 3, "sample_dates": ["1996-08-12", "1997-04-15", "1997-10-21"], "shared_flight_count": 3}	2026-02-05 22:53:03
317	2	148	traveled_with	2	1996-08-12	1999-11-28	{"total_dates": 2, "sample_dates": ["1996-08-12", "1999-11-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
318	2	149	traveled_with	1	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
319	2	150	traveled_with	2	1996-08-18	1997-04-17	{"total_dates": 2, "sample_dates": ["1996-08-18", "1997-04-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
320	2	151	traveled_with	1	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
321	2	153	traveled_with	6	1996-08-21	1997-02-13	{"total_dates": 5, "sample_dates": ["1996-08-21", "1996-08-26", "1996-12-20", "1996-12-23", "1997-02-13"], "shared_flight_count": 6}	2026-02-05 22:53:03
322	2	155	traveled_with	22	1996-10-06	1997-10-21	{"total_dates": 20, "sample_dates": ["1996-10-06", "1996-10-19", "1996-10-22", "1996-10-31", "1996-11-04", "1996-11-21", "1996-12-09", "1997-01-05", "1997-02-25", "1997-03-27"], "shared_flight_count": 22}	2026-02-05 22:53:03
323	2	156	traveled_with	1	1996-11-15	1996-11-15	{"total_dates": 1, "sample_dates": ["1996-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
324	2	157	traveled_with	1	1998-04-09	1998-04-09	{"total_dates": 1, "sample_dates": ["1998-04-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
325	2	158	traveled_with	2	1996-10-24	2001-10-15	{"total_dates": 2, "sample_dates": ["1996-10-24", "2001-10-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
326	2	159	traveled_with	1	1996-10-25	1996-10-25	{"total_dates": 1, "sample_dates": ["1996-10-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
327	2	160	traveled_with	8	1996-10-27	2001-11-12	{"total_dates": 8, "sample_dates": ["1996-10-27", "1997-03-24", "1998-02-09", "1998-02-12", "2000-05-04", "2001-04-17", "2001-05-28", "2001-11-12"], "shared_flight_count": 8}	2026-02-05 22:53:03
328	2	161	traveled_with	1	1996-10-27	1996-10-27	{"total_dates": 1, "sample_dates": ["1996-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
329	2	168	traveled_with	1	1996-11-15	1996-11-15	{"total_dates": 1, "sample_dates": ["1996-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
330	2	169	traveled_with	1	1996-11-15	1996-11-15	{"total_dates": 1, "sample_dates": ["1996-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
331	2	170	traveled_with	1	1996-11-21	1996-11-21	{"total_dates": 1, "sample_dates": ["1996-11-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
332	2	171	traveled_with	1	1996-12-02	1996-12-02	{"total_dates": 1, "sample_dates": ["1996-12-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
333	2	172	traveled_with	1	1996-12-09	1996-12-09	{"total_dates": 1, "sample_dates": ["1996-12-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
334	2	173	traveled_with	1	1996-12-09	1996-12-09	{"total_dates": 1, "sample_dates": ["1996-12-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
335	2	175	traveled_with	1	1997-01-21	1997-01-21	{"total_dates": 1, "sample_dates": ["1997-01-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
336	2	176	traveled_with	2	1997-01-24	1997-01-25	{"total_dates": 2, "sample_dates": ["1997-01-24", "1997-01-25"], "shared_flight_count": 2}	2026-02-05 22:53:03
337	2	178	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
338	2	179	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
339	2	180	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
340	2	184	traveled_with	1	1997-02-25	1997-02-25	{"total_dates": 1, "sample_dates": ["1997-02-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
341	2	186	traveled_with	1	1997-03-24	1997-03-24	{"total_dates": 1, "sample_dates": ["1997-03-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
342	2	187	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
343	2	188	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
344	2	190	traveled_with	2	1999-07-25	2001-09-15	{"total_dates": 2, "sample_dates": ["1999-07-25", "2001-09-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
345	2	191	traveled_with	1	1997-05-09	1997-05-09	{"total_dates": 1, "sample_dates": ["1997-05-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
346	2	192	traveled_with	2	1997-05-15	1997-09-26	{"total_dates": 2, "sample_dates": ["1997-05-15", "1997-09-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
347	2	199	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
348	2	200	traveled_with	9	1997-09-26	2001-03-08	{"total_dates": 6, "sample_dates": ["1997-09-26", "1998-05-18", "1998-05-20", "1998-09-13", "1999-03-31", "2001-03-08"], "shared_flight_count": 9}	2026-02-05 22:53:03
349	2	201	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
350	2	203	traveled_with	153	1997-10-17	2001-09-22	{"total_dates": 137, "sample_dates": ["1997-10-17", "1997-10-21", "1997-10-27", "1997-10-31", "1997-11-02", "1997-11-04", "1997-12-06", "1997-12-09", "1998-01-03", "1998-01-08"], "shared_flight_count": 153}	2026-02-05 22:53:03
351	2	204	traveled_with	2	1997-11-04	1998-02-28	{"total_dates": 2, "sample_dates": ["1997-11-04", "1998-02-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
352	2	205	traveled_with	1	1997-11-04	1997-11-04	{"total_dates": 1, "sample_dates": ["1997-11-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
353	2	209	traveled_with	4	1998-02-09	1999-09-13	{"total_dates": 4, "sample_dates": ["1998-02-09", "1998-03-23", "1998-09-08", "1999-09-13"], "shared_flight_count": 4}	2026-02-05 22:53:03
354	2	210	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
355	2	211	traveled_with	2	1998-01-03	2001-01-11	{"total_dates": 2, "sample_dates": ["1998-01-03", "2001-01-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
356	2	212	traveled_with	2	1998-01-03	2001-01-11	{"total_dates": 2, "sample_dates": ["1998-01-03", "2001-01-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
357	2	213	traveled_with	3	1998-01-08	1998-03-27	{"total_dates": 3, "sample_dates": ["1998-01-08", "1998-01-10", "1998-03-27"], "shared_flight_count": 3}	2026-02-05 22:53:03
358	2	214	traveled_with	3	1998-01-20	1998-01-25	{"total_dates": 2, "sample_dates": ["1998-01-20", "1998-01-25"], "shared_flight_count": 3}	2026-02-05 22:53:03
359	2	215	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
360	2	216	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
361	2	218	traveled_with	2	1998-02-28	2001-04-17	{"total_dates": 2, "sample_dates": ["1998-02-28", "2001-04-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
362	2	222	traveled_with	5	1998-06-26	2000-07-04	{"total_dates": 5, "sample_dates": ["1998-06-26", "1998-08-07", "1999-10-18", "2000-01-04", "2000-07-04"], "shared_flight_count": 5}	2026-02-05 22:53:03
363	2	225	traveled_with	1	2001-06-15	2001-06-15	{"total_dates": 1, "sample_dates": ["2001-06-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
364	2	235	traveled_with	1	1998-04-24	1998-04-24	{"total_dates": 1, "sample_dates": ["1998-04-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
365	2	236	traveled_with	6	1998-04-24	2001-03-08	{"total_dates": 4, "sample_dates": ["1998-04-24", "1998-09-13", "1999-03-31", "2001-03-08"], "shared_flight_count": 6}	2026-02-05 22:53:03
366	2	237	traveled_with	2	1998-05-03	2001-03-31	{"total_dates": 2, "sample_dates": ["1998-05-03", "2001-03-31"], "shared_flight_count": 2}	2026-02-05 22:53:03
367	2	239	traveled_with	2	1998-05-11	1998-05-20	{"total_dates": 2, "sample_dates": ["1998-05-11", "1998-05-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
368	2	240	traveled_with	2	1998-05-18	1998-05-18	{"total_dates": 1, "sample_dates": ["1998-05-18"], "shared_flight_count": 2}	2026-02-05 22:53:03
369	2	241	traveled_with	2	1998-06-12	1998-06-15	{"total_dates": 2, "sample_dates": ["1998-06-12", "1998-06-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
370	2	242	traveled_with	1	1998-06-18	1998-06-18	{"total_dates": 1, "sample_dates": ["1998-06-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
371	2	243	traveled_with	1	1998-06-18	1998-06-18	{"total_dates": 1, "sample_dates": ["1998-06-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
372	2	245	traveled_with	12	1998-06-26	2005-02-19	{"total_dates": 11, "sample_dates": ["1998-06-26", "2000-07-19", "2000-10-21", "2000-10-23", "2001-03-05", "2001-03-06", "2001-07-08", "2001-07-11", "2003-08-10", "2003-10-19"], "shared_flight_count": 12}	2026-02-05 22:53:03
373	2	247	traveled_with	8	1998-08-03	2001-08-19	{"total_dates": 8, "sample_dates": ["1998-08-03", "1998-08-21", "1998-10-09", "1998-10-12", "1998-11-20", "1999-05-27", "2001-08-16", "2001-08-19"], "shared_flight_count": 8}	2026-02-05 22:53:03
374	2	248	traveled_with	1	1998-08-03	1998-08-03	{"total_dates": 1, "sample_dates": ["1998-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
375	2	250	traveled_with	2	2000-09-21	2001-03-22	{"total_dates": 2, "sample_dates": ["2000-09-21", "2001-03-22"], "shared_flight_count": 2}	2026-02-05 22:53:03
376	2	251	traveled_with	1	2005-12-21	2005-12-21	{"total_dates": 1, "sample_dates": ["2005-12-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
377	2	256	traveled_with	7	1998-11-15	2000-02-02	{"total_dates": 5, "sample_dates": ["1998-11-15", "1998-11-16", "1999-03-31", "2000-01-31", "2000-02-02"], "shared_flight_count": 7}	2026-02-05 22:53:03
378	2	258	traveled_with	6	1999-05-10	1999-06-15	{"total_dates": 5, "sample_dates": ["1999-05-10", "1999-05-23", "1999-06-04", "1999-06-07", "1999-06-15"], "shared_flight_count": 6}	2026-02-05 22:53:03
379	2	259	traveled_with	2	1999-03-31	1999-03-31	{"total_dates": 1, "sample_dates": ["1999-03-31"], "shared_flight_count": 2}	2026-02-05 22:53:03
380	2	260	traveled_with	6	1999-04-08	2001-05-07	{"total_dates": 4, "sample_dates": ["1999-04-08", "1999-04-11", "1999-05-10", "2001-05-07"], "shared_flight_count": 6}	2026-02-05 22:53:03
381	2	261	traveled_with	1	1999-04-08	1999-04-08	{"total_dates": 1, "sample_dates": ["1999-04-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
382	2	262	traveled_with	1	1999-04-11	1999-04-11	{"total_dates": 1, "sample_dates": ["1999-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
383	2	263	traveled_with	1	1999-04-11	1999-04-11	{"total_dates": 1, "sample_dates": ["1999-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
384	2	265	traveled_with	10	2000-05-12	2001-10-23	{"total_dates": 7, "sample_dates": ["2000-05-12", "2001-01-06", "2001-03-15", "2001-03-16", "2001-03-19", "2001-03-22", "2001-10-23"], "shared_flight_count": 10}	2026-02-05 22:53:03
385	2	267	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
386	2	268	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
387	2	269	traveled_with	1	1999-08-07	1999-08-07	{"total_dates": 1, "sample_dates": ["1999-08-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
388	2	270	traveled_with	1	1999-11-30	1999-11-30	{"total_dates": 1, "sample_dates": ["1999-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
389	2	273	traveled_with	2	1999-09-25	1999-09-26	{"total_dates": 2, "sample_dates": ["1999-09-25", "1999-09-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
390	2	274	traveled_with	4	1999-10-14	1999-10-18	{"total_dates": 3, "sample_dates": ["1999-10-14", "1999-10-16", "1999-10-18"], "shared_flight_count": 4}	2026-02-05 22:53:03
391	2	277	traveled_with	1	1999-11-22	1999-11-22	{"total_dates": 1, "sample_dates": ["1999-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
392	2	280	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
393	2	281	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
394	2	282	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
395	2	283	traveled_with	1	2000-05-12	2000-05-12	{"total_dates": 1, "sample_dates": ["2000-05-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
396	2	285	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
397	2	289	traveled_with	1	2000-07-19	2000-07-19	{"total_dates": 1, "sample_dates": ["2000-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
398	2	297	traveled_with	7	2000-10-21	2000-12-09	{"total_dates": 5, "sample_dates": ["2000-10-21", "2000-12-05", "2000-12-06", "2000-12-07", "2000-12-09"], "shared_flight_count": 7}	2026-02-05 22:53:03
399	2	298	traveled_with	2	2000-09-10	2000-09-12	{"total_dates": 2, "sample_dates": ["2000-09-10", "2000-09-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
400	2	301	traveled_with	3	2000-10-21	2001-03-08	{"total_dates": 3, "sample_dates": ["2000-10-21", "2000-12-01", "2001-03-08"], "shared_flight_count": 3}	2026-02-05 22:53:03
401	2	303	traveled_with	1	2000-12-07	2000-12-07	{"total_dates": 1, "sample_dates": ["2000-12-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
402	2	304	traveled_with	1	2000-12-07	2000-12-07	{"total_dates": 1, "sample_dates": ["2000-12-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
403	2	305	traveled_with	4	2001-01-06	2003-08-10	{"total_dates": 4, "sample_dates": ["2001-01-06", "2001-03-16", "2001-03-19", "2003-08-10"], "shared_flight_count": 4}	2026-02-05 22:53:03
404	2	306	traveled_with	12	2001-01-11	2001-03-27	{"total_dates": 9, "sample_dates": ["2001-01-11", "2001-03-08", "2001-03-09", "2001-03-11", "2001-03-15", "2001-03-16", "2001-03-19", "2001-03-22", "2001-03-27"], "shared_flight_count": 12}	2026-02-05 22:53:03
405	2	331	traveled_with	20	2001-03-15	2001-09-09	{"total_dates": 17, "sample_dates": ["2001-03-15", "2001-03-16", "2001-03-19", "2001-03-27", "2001-03-29", "2001-04-11", "2001-04-16", "2001-04-17", "2001-04-20", "2001-05-14"], "shared_flight_count": 20}	2026-02-05 22:53:03
406	2	332	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
407	2	333	traveled_with	3	2001-03-16	2001-06-28	{"total_dates": 2, "sample_dates": ["2001-03-16", "2001-06-28"], "shared_flight_count": 3}	2026-02-05 22:53:03
408	2	334	traveled_with	1	2001-03-19	2001-03-19	{"total_dates": 1, "sample_dates": ["2001-03-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
409	2	336	traveled_with	2	2001-03-29	2001-03-31	{"total_dates": 2, "sample_dates": ["2001-03-29", "2001-03-31"], "shared_flight_count": 2}	2026-02-05 22:53:03
410	2	337	traveled_with	3	2001-03-29	2001-04-23	{"total_dates": 3, "sample_dates": ["2001-03-29", "2001-03-31", "2001-04-23"], "shared_flight_count": 3}	2026-02-05 22:53:03
411	2	340	traveled_with	1	2001-04-11	2001-04-11	{"total_dates": 1, "sample_dates": ["2001-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
412	2	341	traveled_with	1	2001-04-17	2001-04-17	{"total_dates": 1, "sample_dates": ["2001-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
413	2	342	traveled_with	2	2001-04-23	2001-04-23	{"total_dates": 1, "sample_dates": ["2001-04-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
414	2	355	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
415	2	356	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
416	2	357	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
417	2	358	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
418	2	359	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
419	2	360	traveled_with	3	2001-06-15	2001-10-23	{"total_dates": 3, "sample_dates": ["2001-06-15", "2001-07-08", "2001-10-23"], "shared_flight_count": 3}	2026-02-05 22:53:03
420	2	361	traveled_with	2	2001-06-22	2001-12-13	{"total_dates": 2, "sample_dates": ["2001-06-22", "2001-12-13"], "shared_flight_count": 2}	2026-02-05 22:53:03
421	2	362	traveled_with	1	2001-06-22	2001-06-22	{"total_dates": 1, "sample_dates": ["2001-06-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
422	2	363	traveled_with	1	2001-08-05	2001-08-05	{"total_dates": 1, "sample_dates": ["2001-08-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
423	2	368	traveled_with	4	2001-08-16	2001-12-26	{"total_dates": 3, "sample_dates": ["2001-08-16", "2001-08-19", "2001-12-26"], "shared_flight_count": 4}	2026-02-05 22:53:03
424	2	369	traveled_with	1	2001-08-16	2001-08-16	{"total_dates": 1, "sample_dates": ["2001-08-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
425	2	370	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
426	2	371	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
427	2	372	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
428	2	374	traveled_with	1	2001-09-03	2001-09-03	{"total_dates": 1, "sample_dates": ["2001-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
429	2	375	traveled_with	1	2001-09-15	2001-09-15	{"total_dates": 1, "sample_dates": ["2001-09-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
430	2	376	traveled_with	1	2001-10-15	2001-10-15	{"total_dates": 1, "sample_dates": ["2001-10-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
431	2	378	traveled_with	1	2001-11-12	2001-11-12	{"total_dates": 1, "sample_dates": ["2001-11-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
432	2	380	traveled_with	1	2001-11-15	2001-11-15	{"total_dates": 1, "sample_dates": ["2001-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
433	2	382	traveled_with	1	2001-12-13	2001-12-13	{"total_dates": 1, "sample_dates": ["2001-12-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
434	2	383	traveled_with	1	2001-12-13	2001-12-13	{"total_dates": 1, "sample_dates": ["2001-12-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
435	2	384	traveled_with	2	2001-12-26	2001-12-26	{"total_dates": 1, "sample_dates": ["2001-12-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
436	2	387	traveled_with	11	2003-08-10	2004-04-22	{"total_dates": 10, "sample_dates": ["2003-08-10", "2003-08-13", "2003-08-31", "2003-10-11", "2003-10-14", "2003-10-16", "2003-10-19", "2003-11-25", "2004-04-11", "2004-04-22"], "shared_flight_count": 11}	2026-02-05 22:53:03
437	2	388	traveled_with	2	2003-08-31	2004-11-28	{"total_dates": 2, "sample_dates": ["2003-08-31", "2004-11-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
438	2	391	traveled_with	9	2003-08-10	2003-11-09	{"total_dates": 6, "sample_dates": ["2003-08-10", "2003-08-13", "2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 9}	2026-02-05 22:53:03
439	2	394	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
440	2	395	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
441	2	396	traveled_with	1	2003-08-22	2003-08-22	{"total_dates": 1, "sample_dates": ["2003-08-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
442	2	398	traveled_with	20	2004-01-02	2006-01-19	{"total_dates": 18, "sample_dates": ["2004-01-02", "2004-01-03", "2004-02-17", "2004-03-01", "2004-04-11", "2004-04-22", "2004-05-05", "2004-05-08", "2004-05-10", "2004-05-12"], "shared_flight_count": 20}	2026-02-05 22:53:03
443	2	399	traveled_with	8	2003-10-11	2004-08-25	{"total_dates": 7, "sample_dates": ["2003-10-11", "2004-02-17", "2004-03-01", "2004-04-11", "2004-04-22", "2004-08-24", "2004-08-25"], "shared_flight_count": 8}	2026-02-05 22:53:03
444	2	404	traveled_with	1	2003-10-11	2003-10-11	{"total_dates": 1, "sample_dates": ["2003-10-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
445	2	405	traveled_with	1	2003-10-19	2003-10-19	{"total_dates": 1, "sample_dates": ["2003-10-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
446	2	406	traveled_with	4	2003-11-05	2003-11-09	{"total_dates": 3, "sample_dates": ["2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
447	2	407	traveled_with	3	2003-11-05	2003-11-09	{"total_dates": 3, "sample_dates": ["2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 3}	2026-02-05 22:53:03
448	2	408	traveled_with	2	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
449	2	409	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
450	2	410	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
451	2	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
452	2	418	traveled_with	3	2003-12-24	2004-01-02	{"total_dates": 3, "sample_dates": ["2003-12-24", "2003-12-26", "2004-01-02"], "shared_flight_count": 3}	2026-02-05 22:53:03
453	2	419	traveled_with	1	2003-12-24	2003-12-24	{"total_dates": 1, "sample_dates": ["2003-12-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
454	2	420	traveled_with	1	2003-12-26	2003-12-26	{"total_dates": 1, "sample_dates": ["2003-12-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
455	2	421	traveled_with	1	2004-01-02	2004-01-02	{"total_dates": 1, "sample_dates": ["2004-01-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
456	2	422	traveled_with	29	2004-01-02	2005-12-21	{"total_dates": 22, "sample_dates": ["2004-01-02", "2004-01-03", "2004-02-12", "2004-02-17", "2004-03-01", "2004-04-22", "2004-05-05", "2004-05-08", "2004-05-10", "2004-05-12"], "shared_flight_count": 29}	2026-02-05 22:53:03
457	2	423	traveled_with	2	2004-01-03	2004-01-03	{"total_dates": 1, "sample_dates": ["2004-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
458	2	424	traveled_with	16	2004-02-12	2005-03-31	{"total_dates": 15, "sample_dates": ["2004-02-12", "2004-02-17", "2004-03-01", "2004-04-22", "2004-05-05", "2004-05-08", "2004-05-10", "2004-05-12", "2004-08-24", "2004-08-25"], "shared_flight_count": 16}	2026-02-05 22:53:03
459	2	425	traveled_with	3	2004-02-12	2004-02-17	{"total_dates": 2, "sample_dates": ["2004-02-12", "2004-02-17"], "shared_flight_count": 3}	2026-02-05 22:53:03
460	2	426	traveled_with	1	2004-02-12	2004-02-12	{"total_dates": 1, "sample_dates": ["2004-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
461	2	428	traveled_with	1	2004-12-21	2004-12-21	{"total_dates": 1, "sample_dates": ["2004-12-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
462	2	430	traveled_with	1	2004-04-22	2004-04-22	{"total_dates": 1, "sample_dates": ["2004-04-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
463	2	431	traveled_with	1	2004-05-05	2004-05-05	{"total_dates": 1, "sample_dates": ["2004-05-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
464	2	442	traveled_with	2	2004-11-28	2005-01-03	{"total_dates": 2, "sample_dates": ["2004-11-28", "2005-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
465	2	450	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
466	2	452	traveled_with	1	2005-03-31	2005-03-31	{"total_dates": 1, "sample_dates": ["2005-03-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
467	2	456	traveled_with	1	2005-02-19	2005-02-19	{"total_dates": 1, "sample_dates": ["2005-02-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
468	2	457	traveled_with	1	2005-09-05	2005-09-05	{"total_dates": 1, "sample_dates": ["2005-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
469	2	458	traveled_with	3	2005-03-08	2005-03-14	{"total_dates": 3, "sample_dates": ["2005-03-08", "2005-03-13", "2005-03-14"], "shared_flight_count": 3}	2026-02-05 22:53:03
470	2	459	traveled_with	2	2005-11-02	2005-11-02	{"total_dates": 1, "sample_dates": ["2005-11-02"], "shared_flight_count": 2}	2026-02-05 22:53:03
471	2	460	traveled_with	2	2005-07-20	2005-07-20	{"total_dates": 1, "sample_dates": ["2005-07-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
472	2	461	traveled_with	2	2005-07-20	2005-07-20	{"total_dates": 1, "sample_dates": ["2005-07-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
473	2	464	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
474	2	465	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
475	2	469	traveled_with	1	2006-01-19	2006-01-19	{"total_dates": 1, "sample_dates": ["2006-01-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
476	2	472	traveled_with	1	2005-12-21	2005-12-21	{"total_dates": 1, "sample_dates": ["2005-12-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
477	6	10	traveled_with	2	2004-10-16	2004-10-17	{"total_dates": 2, "sample_dates": ["2004-10-16", "2004-10-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
478	6	203	traveled_with	1	2000-05-12	2000-05-12	{"total_dates": 1, "sample_dates": ["2000-05-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
479	6	265	traveled_with	1	2000-05-12	2000-05-12	{"total_dates": 1, "sample_dates": ["2000-05-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
480	6	283	traveled_with	1	2000-05-12	2000-05-12	{"total_dates": 1, "sample_dates": ["2000-05-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
481	6	398	traveled_with	2	2004-10-16	2004-10-17	{"total_dates": 2, "sample_dates": ["2004-10-16", "2004-10-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
482	6	422	traveled_with	2	2004-10-16	2004-10-17	{"total_dates": 2, "sample_dates": ["2004-10-16", "2004-10-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
483	6	424	traveled_with	2	2004-10-16	2004-10-17	{"total_dates": 2, "sample_dates": ["2004-10-16", "2004-10-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
484	7	10	traveled_with	1	2004-02-05	2004-02-05	{"total_dates": 1, "sample_dates": ["2004-02-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
485	7	127	traveled_with	1	1998-02-09	1998-02-09	{"total_dates": 1, "sample_dates": ["1998-02-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
486	7	152	traveled_with	1	1997-01-11	1997-01-11	{"total_dates": 1, "sample_dates": ["1997-01-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
487	7	154	traveled_with	1	1996-09-08	1996-09-08	{"total_dates": 1, "sample_dates": ["1996-09-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
488	7	160	traveled_with	1	1998-02-09	1998-02-09	{"total_dates": 1, "sample_dates": ["1998-02-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
489	7	174	traveled_with	1	1997-01-11	1997-01-11	{"total_dates": 1, "sample_dates": ["1997-01-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
490	7	203	traveled_with	2	1998-02-09	1999-04-16	{"total_dates": 2, "sample_dates": ["1998-02-09", "1999-04-16"], "shared_flight_count": 2}	2026-02-05 22:53:03
491	7	209	traveled_with	1	1998-02-09	1998-02-09	{"total_dates": 1, "sample_dates": ["1998-02-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
492	7	422	traveled_with	5	2004-02-05	2005-11-17	{"total_dates": 2, "sample_dates": ["2004-02-05", "2005-11-17"], "shared_flight_count": 5}	2026-02-05 22:53:03
493	7	459	traveled_with	1	2005-11-17	2005-11-17	{"total_dates": 1, "sample_dates": ["2005-11-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
494	8	81	traveled_with	18	1995-11-21	2004-04-11	{"total_dates": 17, "sample_dates": ["1995-11-21", "1995-11-26", "1996-04-08", "1996-11-07", "1996-11-17", "1997-02-17", "1997-04-17", "1997-08-20", "1997-10-31", "1997-12-14"], "shared_flight_count": 18}	2026-02-05 22:53:03
495	8	107	traveled_with	18	1995-11-21	2004-04-11	{"total_dates": 17, "sample_dates": ["1995-11-21", "1995-11-26", "1996-04-08", "1996-11-07", "1996-11-17", "1997-02-17", "1997-04-17", "1997-08-20", "1997-10-31", "1997-12-14"], "shared_flight_count": 18}	2026-02-05 22:53:03
496	8	109	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
497	8	110	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
498	8	111	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
499	8	112	traveled_with	1	1998-02-06	1998-02-06	{"total_dates": 1, "sample_dates": ["1998-02-06"], "shared_flight_count": 1}	2026-02-05 22:53:03
500	8	113	traveled_with	2	1997-04-17	1998-05-03	{"total_dates": 2, "sample_dates": ["1997-04-17", "1998-05-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
501	8	118	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
502	8	119	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
503	8	129	traveled_with	1	1996-11-07	1996-11-07	{"total_dates": 1, "sample_dates": ["1996-11-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
504	8	148	traveled_with	1	1999-11-28	1999-11-28	{"total_dates": 1, "sample_dates": ["1999-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
505	8	150	traveled_with	1	1997-04-17	1997-04-17	{"total_dates": 1, "sample_dates": ["1997-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
506	8	152	traveled_with	1	1997-08-20	1997-08-20	{"total_dates": 1, "sample_dates": ["1997-08-20"], "shared_flight_count": 1}	2026-02-05 22:53:03
507	8	155	traveled_with	2	1997-04-17	1997-08-20	{"total_dates": 2, "sample_dates": ["1997-04-17", "1997-08-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
508	8	157	traveled_with	2	1996-11-07	1998-04-09	{"total_dates": 2, "sample_dates": ["1996-11-07", "1998-04-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
509	8	167	traveled_with	1	1996-11-07	1996-11-07	{"total_dates": 1, "sample_dates": ["1996-11-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
510	8	179	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
511	8	180	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
512	8	203	traveled_with	6	1997-10-31	1999-11-28	{"total_dates": 6, "sample_dates": ["1997-10-31", "1998-01-03", "1998-02-06", "1998-05-01", "1998-05-03", "1999-11-28"], "shared_flight_count": 6}	2026-02-05 22:53:03
513	8	208	traveled_with	1	1997-12-14	1997-12-14	{"total_dates": 1, "sample_dates": ["1997-12-14"], "shared_flight_count": 1}	2026-02-05 22:53:03
514	8	211	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
515	8	212	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
516	8	237	traveled_with	1	1998-05-03	1998-05-03	{"total_dates": 1, "sample_dates": ["1998-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
517	8	387	traveled_with	2	2003-11-25	2004-04-11	{"total_dates": 2, "sample_dates": ["2003-11-25", "2004-04-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
518	8	398	traveled_with	1	2004-04-11	2004-04-11	{"total_dates": 1, "sample_dates": ["2004-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
519	8	399	traveled_with	1	2004-04-11	2004-04-11	{"total_dates": 1, "sample_dates": ["2004-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
520	9	10	traveled_with	9	2003-07-02	2005-02-03	{"total_dates": 7, "sample_dates": ["2003-07-02", "2004-01-05", "2004-01-08", "2004-02-02", "2004-07-15", "2005-01-01", "2005-02-03"], "shared_flight_count": 9}	2026-02-05 22:53:03
521	9	203	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
522	9	280	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
523	9	281	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
524	9	282	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
525	9	387	traveled_with	2	2003-07-02	2004-02-02	{"total_dates": 2, "sample_dates": ["2003-07-02", "2004-02-02"], "shared_flight_count": 2}	2026-02-05 22:53:03
526	9	388	traveled_with	1	2003-07-02	2003-07-02	{"total_dates": 1, "sample_dates": ["2003-07-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
527	9	390	traveled_with	1	2003-07-02	2003-07-02	{"total_dates": 1, "sample_dates": ["2003-07-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
528	9	398	traveled_with	11	2004-01-02	2005-02-03	{"total_dates": 8, "sample_dates": ["2004-01-02", "2004-02-02", "2004-02-17", "2004-04-02", "2004-05-12", "2004-07-15", "2005-01-01", "2005-02-03"], "shared_flight_count": 11}	2026-02-05 22:53:03
529	9	399	traveled_with	4	2004-02-02	2004-04-02	{"total_dates": 3, "sample_dates": ["2004-02-02", "2004-02-17", "2004-04-02"], "shared_flight_count": 4}	2026-02-05 22:53:03
530	9	418	traveled_with	4	2004-01-02	2004-07-15	{"total_dates": 4, "sample_dates": ["2004-01-02", "2004-01-05", "2004-01-08", "2004-07-15"], "shared_flight_count": 4}	2026-02-05 22:53:03
531	9	421	traveled_with	1	2004-01-02	2004-01-02	{"total_dates": 1, "sample_dates": ["2004-01-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
532	9	422	traveled_with	14	2004-01-02	2005-02-03	{"total_dates": 11, "sample_dates": ["2004-01-02", "2004-01-05", "2004-01-08", "2004-02-02", "2004-02-12", "2004-02-17", "2004-04-02", "2004-05-12", "2004-07-15", "2005-01-01"], "shared_flight_count": 14}	2026-02-05 22:53:03
533	9	424	traveled_with	7	2004-02-12	2005-02-03	{"total_dates": 5, "sample_dates": ["2004-02-12", "2004-02-17", "2004-04-02", "2004-05-12", "2005-02-03"], "shared_flight_count": 7}	2026-02-05 22:53:03
534	9	425	traveled_with	4	2004-02-02	2004-02-17	{"total_dates": 3, "sample_dates": ["2004-02-02", "2004-02-12", "2004-02-17"], "shared_flight_count": 4}	2026-02-05 22:53:03
535	9	426	traveled_with	1	2004-02-12	2004-02-12	{"total_dates": 1, "sample_dates": ["2004-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
536	9	436	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
537	9	437	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
538	9	442	traveled_with	4	2005-01-01	2005-02-03	{"total_dates": 2, "sample_dates": ["2005-01-01", "2005-02-03"], "shared_flight_count": 4}	2026-02-05 22:53:03
539	9	451	traveled_with	2	2005-01-01	2005-01-01	{"total_dates": 1, "sample_dates": ["2005-01-01"], "shared_flight_count": 2}	2026-02-05 22:53:03
540	9	452	traveled_with	1	2005-02-03	2005-02-03	{"total_dates": 1, "sample_dates": ["2005-02-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
541	10	13	traveled_with	5	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 5}	2026-02-05 22:53:03
542	10	81	traveled_with	2	2004-10-08	2004-10-10	{"total_dates": 2, "sample_dates": ["2004-10-08", "2004-10-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
543	10	107	traveled_with	2	2004-10-08	2004-10-10	{"total_dates": 2, "sample_dates": ["2004-10-08", "2004-10-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
544	10	113	traveled_with	1	2001-11-30	2001-11-30	{"total_dates": 1, "sample_dates": ["2001-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
545	10	158	traveled_with	1	2001-10-15	2001-10-15	{"total_dates": 1, "sample_dates": ["2001-10-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
546	10	160	traveled_with	1	2001-11-30	2001-11-30	{"total_dates": 1, "sample_dates": ["2001-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
547	10	203	traveled_with	2	2001-09-03	2001-10-26	{"total_dates": 2, "sample_dates": ["2001-09-03", "2001-10-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
548	10	218	traveled_with	2	2001-11-30	2004-03-11	{"total_dates": 2, "sample_dates": ["2001-11-30", "2004-03-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
549	10	242	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
550	10	245	traveled_with	7	2003-10-19	2004-08-06	{"total_dates": 5, "sample_dates": ["2003-10-19", "2004-02-09", "2004-07-02", "2004-07-04", "2004-08-06"], "shared_flight_count": 7}	2026-02-05 22:53:03
551	10	251	traveled_with	2	2004-04-15	2005-09-14	{"total_dates": 2, "sample_dates": ["2004-04-15", "2005-09-14"], "shared_flight_count": 2}	2026-02-05 22:53:03
552	10	265	traveled_with	2	2001-01-06	2001-10-23	{"total_dates": 2, "sample_dates": ["2001-01-06", "2001-10-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
553	10	305	traveled_with	1	2001-01-06	2001-01-06	{"total_dates": 1, "sample_dates": ["2001-01-06"], "shared_flight_count": 1}	2026-02-05 22:53:03
554	10	331	traveled_with	1	2001-09-03	2001-09-03	{"total_dates": 1, "sample_dates": ["2001-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
555	10	360	traveled_with	2	2001-10-23	2001-10-26	{"total_dates": 2, "sample_dates": ["2001-10-23", "2001-10-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
556	10	361	traveled_with	2	2001-12-13	2005-11-08	{"total_dates": 2, "sample_dates": ["2001-12-13", "2005-11-08"], "shared_flight_count": 2}	2026-02-05 22:53:03
557	10	368	traveled_with	2	2001-12-26	2001-12-26	{"total_dates": 1, "sample_dates": ["2001-12-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
558	10	374	traveled_with	1	2001-09-03	2001-09-03	{"total_dates": 1, "sample_dates": ["2001-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
559	10	375	traveled_with	1	2001-11-30	2001-11-30	{"total_dates": 1, "sample_dates": ["2001-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
560	10	376	traveled_with	1	2001-10-15	2001-10-15	{"total_dates": 1, "sample_dates": ["2001-10-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
561	10	378	traveled_with	4	2001-10-30	2001-11-09	{"total_dates": 2, "sample_dates": ["2001-10-30", "2001-11-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
562	10	380	traveled_with	1	2001-11-15	2001-11-15	{"total_dates": 1, "sample_dates": ["2001-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
563	10	382	traveled_with	1	2001-12-13	2001-12-13	{"total_dates": 1, "sample_dates": ["2001-12-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
564	10	383	traveled_with	1	2001-12-13	2001-12-13	{"total_dates": 1, "sample_dates": ["2001-12-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
565	10	384	traveled_with	2	2001-12-26	2001-12-26	{"total_dates": 1, "sample_dates": ["2001-12-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
566	10	387	traveled_with	18	2003-07-02	2004-07-22	{"total_dates": 18, "sample_dates": ["2003-07-02", "2003-07-07", "2003-07-31", "2003-09-22", "2003-10-14", "2003-10-16", "2003-10-19", "2003-10-26", "2003-11-14", "2003-11-18"], "shared_flight_count": 18}	2026-02-05 22:53:03
567	10	388	traveled_with	6	2003-07-02	2004-12-03	{"total_dates": 6, "sample_dates": ["2003-07-02", "2003-07-07", "2003-09-22", "2004-11-23", "2004-11-28", "2004-12-03"], "shared_flight_count": 6}	2026-02-05 22:53:03
568	10	390	traveled_with	2	2003-07-02	2003-07-07	{"total_dates": 2, "sample_dates": ["2003-07-02", "2003-07-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
569	10	391	traveled_with	17	2003-07-31	2005-11-08	{"total_dates": 12, "sample_dates": ["2003-07-31", "2003-10-01", "2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09", "2003-11-11", "2003-11-14", "2004-07-11", "2004-11-18"], "shared_flight_count": 17}	2026-02-05 22:53:03
570	10	393	traveled_with	1	2003-07-31	2003-07-31	{"total_dates": 1, "sample_dates": ["2003-07-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
571	10	396	traveled_with	1	2003-08-22	2003-08-22	{"total_dates": 1, "sample_dates": ["2003-08-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
572	10	398	traveled_with	77	2003-09-22	2006-01-19	{"total_dates": 65, "sample_dates": ["2003-09-22", "2003-10-03", "2003-12-07", "2004-01-12", "2004-01-16", "2004-01-20", "2004-01-28", "2004-02-02", "2004-02-19", "2004-02-24"], "shared_flight_count": 77}	2026-02-05 22:53:03
573	10	399	traveled_with	29	2003-09-22	2004-11-14	{"total_dates": 26, "sample_dates": ["2003-09-22", "2003-10-01", "2003-10-03", "2003-10-26", "2003-12-09", "2004-01-12", "2004-01-16", "2004-01-20", "2004-01-28", "2004-02-02"], "shared_flight_count": 29}	2026-02-05 22:53:03
574	10	401	traveled_with	6	2003-10-01	2004-11-14	{"total_dates": 5, "sample_dates": ["2003-10-01", "2004-03-11", "2004-03-13", "2004-03-19", "2004-11-14"], "shared_flight_count": 6}	2026-02-05 22:53:03
575	10	405	traveled_with	1	2003-10-19	2003-10-19	{"total_dates": 1, "sample_dates": ["2003-10-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
576	10	406	traveled_with	5	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 5}	2026-02-05 22:53:03
577	10	407	traveled_with	4	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
578	10	408	traveled_with	2	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
579	10	409	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
580	10	410	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
581	10	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
582	10	412	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
583	10	413	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
584	10	414	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
585	10	416	traveled_with	2	2003-12-07	2003-12-07	{"total_dates": 1, "sample_dates": ["2003-12-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
586	10	418	traveled_with	6	2004-01-05	2004-07-19	{"total_dates": 6, "sample_dates": ["2004-01-05", "2004-01-08", "2004-01-12", "2004-02-09", "2004-07-15", "2004-07-19"], "shared_flight_count": 6}	2026-02-05 22:53:03
587	10	422	traveled_with	85	2004-01-05	2005-11-20	{"total_dates": 74, "sample_dates": ["2004-01-05", "2004-01-08", "2004-01-12", "2004-01-16", "2004-01-20", "2004-01-28", "2004-02-02", "2004-02-05", "2004-02-19", "2004-02-24"], "shared_flight_count": 85}	2026-02-05 22:53:03
588	10	424	traveled_with	55	2004-01-12	2005-11-20	{"total_dates": 51, "sample_dates": ["2004-01-12", "2004-01-16", "2004-01-20", "2004-02-09", "2004-02-19", "2004-02-24", "2004-02-27", "2004-02-29", "2004-03-01", "2004-04-15"], "shared_flight_count": 55}	2026-02-05 22:53:03
589	10	425	traveled_with	1	2004-02-02	2004-02-02	{"total_dates": 1, "sample_dates": ["2004-02-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
590	10	427	traveled_with	1	2004-02-24	2004-02-24	{"total_dates": 1, "sample_dates": ["2004-02-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
591	10	428	traveled_with	2	2004-03-13	2004-12-21	{"total_dates": 2, "sample_dates": ["2004-03-13", "2004-12-21"], "shared_flight_count": 2}	2026-02-05 22:53:03
592	10	429	traveled_with	3	2004-04-19	2004-09-16	{"total_dates": 3, "sample_dates": ["2004-04-19", "2004-08-06", "2004-09-16"], "shared_flight_count": 3}	2026-02-05 22:53:03
593	10	431	traveled_with	1	2004-05-05	2004-05-05	{"total_dates": 1, "sample_dates": ["2004-05-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
594	10	432	traveled_with	1	2004-06-13	2004-06-13	{"total_dates": 1, "sample_dates": ["2004-06-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
595	10	433	traveled_with	2	2004-08-06	2004-08-10	{"total_dates": 2, "sample_dates": ["2004-08-06", "2004-08-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
596	10	434	traveled_with	4	2004-07-02	2004-07-04	{"total_dates": 2, "sample_dates": ["2004-07-02", "2004-07-04"], "shared_flight_count": 4}	2026-02-05 22:53:03
597	10	435	traveled_with	4	2004-07-02	2004-07-04	{"total_dates": 2, "sample_dates": ["2004-07-02", "2004-07-04"], "shared_flight_count": 4}	2026-02-05 22:53:03
598	10	436	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
599	10	437	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
600	10	438	traveled_with	1	2004-07-19	2004-07-19	{"total_dates": 1, "sample_dates": ["2004-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
601	10	439	traveled_with	1	2004-07-22	2004-07-22	{"total_dates": 1, "sample_dates": ["2004-07-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
602	10	440	traveled_with	1	2004-08-03	2004-08-03	{"total_dates": 1, "sample_dates": ["2004-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
603	10	441	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
604	10	442	traveled_with	18	2004-08-10	2005-08-26	{"total_dates": 15, "sample_dates": ["2004-08-10", "2004-09-16", "2004-10-20", "2004-10-25", "2004-11-18", "2004-11-23", "2004-11-28", "2005-01-01", "2005-01-03", "2005-02-03"], "shared_flight_count": 18}	2026-02-05 22:53:03
605	10	449	traveled_with	2	2004-11-09	2004-11-10	{"total_dates": 2, "sample_dates": ["2004-11-09", "2004-11-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
606	10	450	traveled_with	5	2004-12-03	2005-07-05	{"total_dates": 5, "sample_dates": ["2004-12-03", "2005-04-06", "2005-05-24", "2005-06-01", "2005-07-05"], "shared_flight_count": 5}	2026-02-05 22:53:03
607	10	451	traveled_with	2	2005-01-01	2005-01-01	{"total_dates": 1, "sample_dates": ["2005-01-01"], "shared_flight_count": 2}	2026-02-05 22:53:03
608	10	452	traveled_with	5	2005-01-31	2005-04-06	{"total_dates": 5, "sample_dates": ["2005-01-31", "2005-02-03", "2005-03-24", "2005-03-29", "2005-04-06"], "shared_flight_count": 5}	2026-02-05 22:53:03
609	10	457	traveled_with	9	2005-03-24	2005-11-08	{"total_dates": 8, "sample_dates": ["2005-03-24", "2005-03-29", "2005-05-19", "2005-07-22", "2005-07-25", "2005-08-02", "2005-09-14", "2005-11-08"], "shared_flight_count": 9}	2026-02-05 22:53:03
1494	107	8	related_to	1	\N	\N	{"notes": "Eva and Glenn Dubin are married", "original_type": "family", "evidence_relationship_id": 24}	2026-02-05 22:53:03
610	10	459	traveled_with	8	2005-07-22	2005-11-20	{"total_dates": 6, "sample_dates": ["2005-07-22", "2005-07-25", "2005-08-02", "2005-09-24", "2005-11-02", "2005-11-20"], "shared_flight_count": 8}	2026-02-05 22:53:03
611	10	461	traveled_with	1	2005-09-20	2005-09-20	{"total_dates": 1, "sample_dates": ["2005-09-20"], "shared_flight_count": 1}	2026-02-05 22:53:03
612	10	462	traveled_with	2	2005-08-02	2005-09-24	{"total_dates": 2, "sample_dates": ["2005-08-02", "2005-09-24"], "shared_flight_count": 2}	2026-02-05 22:53:03
613	10	463	traveled_with	1	2005-08-02	2005-08-02	{"total_dates": 1, "sample_dates": ["2005-08-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
614	10	466	traveled_with	1	2005-09-24	2005-09-24	{"total_dates": 1, "sample_dates": ["2005-09-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
615	10	467	traveled_with	1	2005-09-25	2005-09-25	{"total_dates": 1, "sample_dates": ["2005-09-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
616	10	469	traveled_with	2	2005-11-08	2006-01-19	{"total_dates": 2, "sample_dates": ["2005-11-08", "2006-01-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
617	13	391	traveled_with	5	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 5}	2026-02-05 22:53:03
618	13	406	traveled_with	5	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 5}	2026-02-05 22:53:03
619	13	407	traveled_with	4	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
620	13	408	traveled_with	2	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
621	13	409	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
622	13	410	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
623	13	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
624	14	81	traveled_with	1	1997-01-05	1997-01-05	{"total_dates": 1, "sample_dates": ["1997-01-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
625	14	107	traveled_with	1	1997-01-05	1997-01-05	{"total_dates": 1, "sample_dates": ["1997-01-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
626	14	155	traveled_with	1	1997-01-05	1997-01-05	{"total_dates": 1, "sample_dates": ["1997-01-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
627	81	107	traveled_with	34	1995-11-21	2005-02-19	{"total_dates": 32, "sample_dates": ["1995-11-21", "1995-11-26", "1996-03-24", "1996-04-08", "1996-11-07", "1996-11-11", "1996-11-17", "1996-12-12", "1997-01-05", "1997-02-13"], "shared_flight_count": 34}	2026-02-05 22:53:03
628	81	109	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
629	81	110	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
630	81	111	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
631	81	112	traveled_with	2	1997-02-13	1998-02-06	{"total_dates": 2, "sample_dates": ["1997-02-13", "1998-02-06"], "shared_flight_count": 2}	2026-02-05 22:53:03
632	81	113	traveled_with	3	1997-04-17	1999-05-27	{"total_dates": 3, "sample_dates": ["1997-04-17", "1998-05-03", "1999-05-27"], "shared_flight_count": 3}	2026-02-05 22:53:03
633	81	118	traveled_with	1	1996-12-12	1996-12-12	{"total_dates": 1, "sample_dates": ["1996-12-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
634	81	119	traveled_with	1	1996-12-12	1996-12-12	{"total_dates": 1, "sample_dates": ["1996-12-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
635	81	123	traveled_with	1	1996-11-11	1996-11-11	{"total_dates": 1, "sample_dates": ["1996-11-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
636	81	129	traveled_with	2	1996-11-07	1996-11-11	{"total_dates": 2, "sample_dates": ["1996-11-07", "1996-11-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
637	81	130	traveled_with	1	1996-03-24	1996-03-24	{"total_dates": 1, "sample_dates": ["1996-03-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
638	81	131	traveled_with	1	1996-05-02	1996-05-02	{"total_dates": 1, "sample_dates": ["1996-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
639	81	132	traveled_with	1	1996-05-02	1996-05-02	{"total_dates": 1, "sample_dates": ["1996-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
640	81	133	traveled_with	1	1996-05-02	1996-05-02	{"total_dates": 1, "sample_dates": ["1996-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
641	81	134	traveled_with	1	1996-05-02	1996-05-02	{"total_dates": 1, "sample_dates": ["1996-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
642	81	148	traveled_with	1	1999-11-28	1999-11-28	{"total_dates": 1, "sample_dates": ["1999-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
643	81	150	traveled_with	1	1997-04-17	1997-04-17	{"total_dates": 1, "sample_dates": ["1997-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
644	81	152	traveled_with	2	1997-08-20	1997-08-23	{"total_dates": 2, "sample_dates": ["1997-08-20", "1997-08-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
645	81	153	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
646	81	155	traveled_with	4	1997-01-05	1997-08-23	{"total_dates": 4, "sample_dates": ["1997-01-05", "1997-04-17", "1997-08-20", "1997-08-23"], "shared_flight_count": 4}	2026-02-05 22:53:03
647	81	157	traveled_with	3	1996-11-07	1998-04-09	{"total_dates": 3, "sample_dates": ["1996-11-07", "1996-11-11", "1998-04-09"], "shared_flight_count": 3}	2026-02-05 22:53:03
648	81	167	traveled_with	2	1996-11-07	1996-11-11	{"total_dates": 2, "sample_dates": ["1996-11-07", "1996-11-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
649	81	178	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
650	81	179	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
651	81	180	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
652	81	203	traveled_with	8	1997-10-31	2000-01-04	{"total_dates": 8, "sample_dates": ["1997-10-31", "1998-02-06", "1998-05-01", "1998-05-03", "1999-03-25", "1999-05-27", "1999-11-28", "2000-01-04"], "shared_flight_count": 8}	2026-02-05 22:53:03
653	81	208	traveled_with	1	1997-12-14	1997-12-14	{"total_dates": 1, "sample_dates": ["1997-12-14"], "shared_flight_count": 1}	2026-02-05 22:53:03
654	81	209	traveled_with	1	1998-03-23	1998-03-23	{"total_dates": 1, "sample_dates": ["1998-03-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
655	81	215	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
656	81	222	traveled_with	1	2000-01-04	2000-01-04	{"total_dates": 1, "sample_dates": ["2000-01-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
657	81	237	traveled_with	1	1998-05-03	1998-05-03	{"total_dates": 1, "sample_dates": ["1998-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
658	81	245	traveled_with	1	2005-02-19	2005-02-19	{"total_dates": 1, "sample_dates": ["2005-02-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
659	81	247	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
660	81	250	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
661	81	265	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
662	81	267	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
663	81	268	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
664	81	306	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
665	81	387	traveled_with	2	2003-11-25	2004-04-11	{"total_dates": 2, "sample_dates": ["2003-11-25", "2004-04-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
666	81	398	traveled_with	5	2004-01-03	2004-10-10	{"total_dates": 4, "sample_dates": ["2004-01-03", "2004-04-11", "2004-10-08", "2004-10-10"], "shared_flight_count": 5}	2026-02-05 22:53:03
667	81	399	traveled_with	1	2004-04-11	2004-04-11	{"total_dates": 1, "sample_dates": ["2004-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
668	81	422	traveled_with	4	2004-01-03	2004-10-10	{"total_dates": 3, "sample_dates": ["2004-01-03", "2004-10-08", "2004-10-10"], "shared_flight_count": 4}	2026-02-05 22:53:03
669	81	423	traveled_with	2	2004-01-03	2004-01-03	{"total_dates": 1, "sample_dates": ["2004-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
670	81	424	traveled_with	2	2004-10-08	2004-10-10	{"total_dates": 2, "sample_dates": ["2004-10-08", "2004-10-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
671	81	456	traveled_with	1	2005-02-19	2005-02-19	{"total_dates": 1, "sample_dates": ["2005-02-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
672	85	113	traveled_with	1	2001-04-16	2001-04-16	{"total_dates": 1, "sample_dates": ["2001-04-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
673	85	200	traveled_with	2	2001-03-08	2001-03-08	{"total_dates": 1, "sample_dates": ["2001-03-08"], "shared_flight_count": 2}	2026-02-05 22:53:03
674	85	203	traveled_with	14	2000-12-11	2001-07-16	{"total_dates": 12, "sample_dates": ["2000-12-11", "2001-01-26", "2001-03-05", "2001-03-06", "2001-03-08", "2001-03-09", "2001-03-11", "2001-03-27", "2001-05-14", "2001-07-08"], "shared_flight_count": 14}	2026-02-05 22:53:03
675	85	236	traveled_with	2	2001-03-08	2001-03-08	{"total_dates": 1, "sample_dates": ["2001-03-08"], "shared_flight_count": 2}	2026-02-05 22:53:03
676	85	245	traveled_with	5	2001-03-05	2001-07-11	{"total_dates": 5, "sample_dates": ["2001-03-05", "2001-03-06", "2001-05-05", "2001-07-08", "2001-07-11"], "shared_flight_count": 5}	2026-02-05 22:53:03
677	85	301	traveled_with	1	2001-03-08	2001-03-08	{"total_dates": 1, "sample_dates": ["2001-03-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
678	85	306	traveled_with	5	2001-03-08	2001-03-27	{"total_dates": 4, "sample_dates": ["2001-03-08", "2001-03-09", "2001-03-11", "2001-03-27"], "shared_flight_count": 5}	2026-02-05 22:53:03
679	85	331	traveled_with	6	2001-03-27	2001-06-05	{"total_dates": 6, "sample_dates": ["2001-03-27", "2001-04-11", "2001-04-16", "2001-05-14", "2001-06-03", "2001-06-05"], "shared_flight_count": 6}	2026-02-05 22:53:03
680	85	340	traveled_with	1	2001-04-11	2001-04-11	{"total_dates": 1, "sample_dates": ["2001-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
681	85	360	traveled_with	1	2001-07-08	2001-07-08	{"total_dates": 1, "sample_dates": ["2001-07-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
682	107	109	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
683	107	110	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
684	107	111	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
685	107	112	traveled_with	3	1996-03-22	1998-02-06	{"total_dates": 3, "sample_dates": ["1996-03-22", "1997-02-13", "1998-02-06"], "shared_flight_count": 3}	2026-02-05 22:53:03
686	107	113	traveled_with	3	1997-04-17	1999-05-27	{"total_dates": 3, "sample_dates": ["1997-04-17", "1998-05-03", "1999-05-27"], "shared_flight_count": 3}	2026-02-05 22:53:03
687	107	118	traveled_with	2	1996-12-12	1998-01-03	{"total_dates": 2, "sample_dates": ["1996-12-12", "1998-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
688	107	119	traveled_with	2	1996-12-12	1998-01-03	{"total_dates": 2, "sample_dates": ["1996-12-12", "1998-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
689	107	123	traveled_with	1	1996-11-11	1996-11-11	{"total_dates": 1, "sample_dates": ["1996-11-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
690	107	128	traveled_with	1	1996-03-22	1996-03-22	{"total_dates": 1, "sample_dates": ["1996-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
691	107	129	traveled_with	3	1996-03-22	1996-11-11	{"total_dates": 3, "sample_dates": ["1996-03-22", "1996-11-07", "1996-11-11"], "shared_flight_count": 3}	2026-02-05 22:53:03
692	107	130	traveled_with	1	1996-03-24	1996-03-24	{"total_dates": 1, "sample_dates": ["1996-03-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
693	107	148	traveled_with	1	1999-11-28	1999-11-28	{"total_dates": 1, "sample_dates": ["1999-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
694	107	150	traveled_with	1	1997-04-17	1997-04-17	{"total_dates": 1, "sample_dates": ["1997-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
695	107	152	traveled_with	2	1997-08-20	1997-08-23	{"total_dates": 2, "sample_dates": ["1997-08-20", "1997-08-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
696	107	153	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
697	107	155	traveled_with	4	1997-01-05	1997-08-23	{"total_dates": 4, "sample_dates": ["1997-01-05", "1997-04-17", "1997-08-20", "1997-08-23"], "shared_flight_count": 4}	2026-02-05 22:53:03
698	107	157	traveled_with	3	1996-11-07	1998-04-09	{"total_dates": 3, "sample_dates": ["1996-11-07", "1996-11-11", "1998-04-09"], "shared_flight_count": 3}	2026-02-05 22:53:03
699	107	167	traveled_with	2	1996-11-07	1996-11-11	{"total_dates": 2, "sample_dates": ["1996-11-07", "1996-11-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
700	107	178	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
701	107	179	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
702	107	180	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
703	107	203	traveled_with	8	1997-10-31	2000-01-04	{"total_dates": 8, "sample_dates": ["1997-10-31", "1998-01-03", "1998-02-06", "1998-05-03", "1999-03-25", "1999-05-27", "1999-11-28", "2000-01-04"], "shared_flight_count": 8}	2026-02-05 22:53:03
704	107	208	traveled_with	1	1997-12-14	1997-12-14	{"total_dates": 1, "sample_dates": ["1997-12-14"], "shared_flight_count": 1}	2026-02-05 22:53:03
705	107	209	traveled_with	1	1998-03-23	1998-03-23	{"total_dates": 1, "sample_dates": ["1998-03-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
706	107	211	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
707	107	212	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
708	107	215	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
709	107	222	traveled_with	1	2000-01-04	2000-01-04	{"total_dates": 1, "sample_dates": ["2000-01-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
710	107	237	traveled_with	1	1998-05-03	1998-05-03	{"total_dates": 1, "sample_dates": ["1998-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
711	107	245	traveled_with	1	2005-02-19	2005-02-19	{"total_dates": 1, "sample_dates": ["2005-02-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
712	107	247	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
713	107	250	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
714	107	265	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
715	107	267	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
716	107	268	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
717	107	306	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
718	107	387	traveled_with	2	2003-11-25	2004-04-11	{"total_dates": 2, "sample_dates": ["2003-11-25", "2004-04-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
719	107	398	traveled_with	5	2004-01-03	2004-10-10	{"total_dates": 4, "sample_dates": ["2004-01-03", "2004-04-11", "2004-10-08", "2004-10-10"], "shared_flight_count": 5}	2026-02-05 22:53:03
720	107	399	traveled_with	1	2004-04-11	2004-04-11	{"total_dates": 1, "sample_dates": ["2004-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
721	107	422	traveled_with	4	2004-01-03	2004-10-10	{"total_dates": 3, "sample_dates": ["2004-01-03", "2004-10-08", "2004-10-10"], "shared_flight_count": 4}	2026-02-05 22:53:03
722	107	423	traveled_with	2	2004-01-03	2004-01-03	{"total_dates": 1, "sample_dates": ["2004-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
723	107	424	traveled_with	2	2004-10-08	2004-10-10	{"total_dates": 2, "sample_dates": ["2004-10-08", "2004-10-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
724	107	456	traveled_with	1	2005-02-19	2005-02-19	{"total_dates": 1, "sample_dates": ["2005-02-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
725	109	110	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
726	109	111	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
727	110	111	traveled_with	1	1995-11-26	1995-11-26	{"total_dates": 1, "sample_dates": ["1995-11-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
728	112	118	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
729	112	119	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
730	112	120	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
731	112	121	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
732	112	122	traveled_with	1	1996-02-15	1996-02-15	{"total_dates": 1, "sample_dates": ["1996-02-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
733	112	123	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
734	112	124	traveled_with	1	1996-03-04	1996-03-04	{"total_dates": 1, "sample_dates": ["1996-03-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
735	112	128	traveled_with	1	1996-03-22	1996-03-22	{"total_dates": 1, "sample_dates": ["1996-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
736	112	129	traveled_with	1	1996-03-22	1996-03-22	{"total_dates": 1, "sample_dates": ["1996-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
737	112	139	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
738	112	152	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
739	112	153	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
740	112	160	traveled_with	1	2000-01-10	2000-01-10	{"total_dates": 1, "sample_dates": ["2000-01-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
741	112	178	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
742	112	181	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
743	112	182	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
744	112	183	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
745	112	192	traveled_with	1	1997-05-15	1997-05-15	{"total_dates": 1, "sample_dates": ["1997-05-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
746	112	203	traveled_with	4	1998-02-06	2000-07-19	{"total_dates": 4, "sample_dates": ["1998-02-06", "2000-06-30", "2000-07-04", "2000-07-19"], "shared_flight_count": 4}	2026-02-05 22:53:03
747	112	222	traveled_with	1	2000-07-04	2000-07-04	{"total_dates": 1, "sample_dates": ["2000-07-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
748	112	245	traveled_with	1	2000-07-19	2000-07-19	{"total_dates": 1, "sample_dates": ["2000-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
749	112	257	traveled_with	2	1999-05-02	2000-01-16	{"total_dates": 2, "sample_dates": ["1999-05-02", "2000-01-16"], "shared_flight_count": 2}	2026-02-05 22:53:03
750	112	258	traveled_with	1	1999-05-02	1999-05-02	{"total_dates": 1, "sample_dates": ["1999-05-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
751	112	273	traveled_with	1	2000-01-12	2000-01-12	{"total_dates": 1, "sample_dates": ["2000-01-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
752	112	289	traveled_with	1	2000-07-19	2000-07-19	{"total_dates": 1, "sample_dates": ["2000-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
753	113	114	traveled_with	1	1996-01-01	1996-01-01	{"total_dates": 1, "sample_dates": ["1996-01-01"], "shared_flight_count": 1}	2026-02-05 22:53:03
754	113	115	traveled_with	1	1996-01-01	1996-01-01	{"total_dates": 1, "sample_dates": ["1996-01-01"], "shared_flight_count": 1}	2026-02-05 22:53:03
755	113	118	traveled_with	1	1997-12-17	1997-12-17	{"total_dates": 1, "sample_dates": ["1997-12-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
756	113	119	traveled_with	1	1997-12-17	1997-12-17	{"total_dates": 1, "sample_dates": ["1997-12-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
757	113	147	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
758	113	150	traveled_with	1	1997-04-17	1997-04-17	{"total_dates": 1, "sample_dates": ["1997-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
759	113	152	traveled_with	1	1997-01-30	1997-01-30	{"total_dates": 1, "sample_dates": ["1997-01-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
760	113	153	traveled_with	2	1996-12-20	1996-12-23	{"total_dates": 2, "sample_dates": ["1996-12-20", "1996-12-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
761	113	155	traveled_with	4	1996-12-04	1997-04-17	{"total_dates": 3, "sample_dates": ["1996-12-04", "1997-04-15", "1997-04-17"], "shared_flight_count": 4}	2026-02-05 22:53:03
762	113	160	traveled_with	1	2001-11-30	2001-11-30	{"total_dates": 1, "sample_dates": ["2001-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
763	113	171	traveled_with	1	1996-12-02	1996-12-02	{"total_dates": 1, "sample_dates": ["1996-12-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
764	113	177	traveled_with	1	1997-01-30	1997-01-30	{"total_dates": 1, "sample_dates": ["1997-01-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
765	113	187	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
766	113	188	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
767	113	189	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
768	113	203	traveled_with	10	1997-12-17	1999-10-27	{"total_dates": 9, "sample_dates": ["1997-12-17", "1998-01-20", "1998-01-25", "1998-02-27", "1998-05-03", "1998-09-19", "1998-10-23", "1999-05-27", "1999-10-27"], "shared_flight_count": 10}	2026-02-05 22:53:03
769	113	209	traveled_with	2	1997-12-17	1997-12-17	{"total_dates": 1, "sample_dates": ["1997-12-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
770	113	210	traveled_with	1	1997-12-17	1997-12-17	{"total_dates": 1, "sample_dates": ["1997-12-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
771	113	214	traveled_with	2	1998-01-20	1998-01-25	{"total_dates": 2, "sample_dates": ["1998-01-20", "1998-01-25"], "shared_flight_count": 2}	2026-02-05 22:53:03
772	113	218	traveled_with	1	2001-11-30	2001-11-30	{"total_dates": 1, "sample_dates": ["2001-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
773	113	237	traveled_with	1	1998-05-03	1998-05-03	{"total_dates": 1, "sample_dates": ["1998-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
774	113	247	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
775	113	250	traveled_with	1	1998-08-25	1998-08-25	{"total_dates": 1, "sample_dates": ["1998-08-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
776	113	251	traveled_with	1	1998-09-19	1998-09-19	{"total_dates": 1, "sample_dates": ["1998-09-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
777	113	258	traveled_with	1	1999-06-15	1999-06-15	{"total_dates": 1, "sample_dates": ["1999-06-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
778	113	267	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
779	113	268	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
780	113	275	traveled_with	1	1999-10-27	1999-10-27	{"total_dates": 1, "sample_dates": ["1999-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
781	113	276	traveled_with	1	1999-10-27	1999-10-27	{"total_dates": 1, "sample_dates": ["1999-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
782	113	331	traveled_with	1	2001-04-16	2001-04-16	{"total_dates": 1, "sample_dates": ["2001-04-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
783	113	375	traveled_with	1	2001-11-30	2001-11-30	{"total_dates": 1, "sample_dates": ["2001-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
784	114	115	traveled_with	1	1996-01-01	1996-01-01	{"total_dates": 1, "sample_dates": ["1996-01-01"], "shared_flight_count": 1}	2026-02-05 22:53:03
785	118	119	traveled_with	6	1996-02-15	1998-02-12	{"total_dates": 6, "sample_dates": ["1996-02-15", "1996-02-19", "1996-12-12", "1997-12-17", "1998-01-03", "1998-02-12"], "shared_flight_count": 6}	2026-02-05 22:53:03
786	118	120	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
787	118	121	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
788	118	122	traveled_with	1	1996-02-15	1996-02-15	{"total_dates": 1, "sample_dates": ["1996-02-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
789	118	123	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
790	118	160	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
791	118	203	traveled_with	2	1998-01-03	1998-02-12	{"total_dates": 2, "sample_dates": ["1998-01-03", "1998-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
792	118	209	traveled_with	1	1997-12-17	1997-12-17	{"total_dates": 1, "sample_dates": ["1997-12-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
793	118	210	traveled_with	2	1997-12-17	1998-02-12	{"total_dates": 2, "sample_dates": ["1997-12-17", "1998-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
794	118	211	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
795	118	212	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
796	118	216	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
797	119	120	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
798	119	121	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
799	119	122	traveled_with	1	1996-02-15	1996-02-15	{"total_dates": 1, "sample_dates": ["1996-02-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
800	119	123	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
801	119	160	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
802	119	203	traveled_with	2	1998-01-03	1998-02-12	{"total_dates": 2, "sample_dates": ["1998-01-03", "1998-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
803	119	209	traveled_with	1	1997-12-17	1997-12-17	{"total_dates": 1, "sample_dates": ["1997-12-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
804	119	210	traveled_with	2	1997-12-17	1998-02-12	{"total_dates": 2, "sample_dates": ["1997-12-17", "1998-02-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
805	119	211	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
806	119	212	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
807	119	216	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
808	120	121	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
809	120	122	traveled_with	1	1996-02-15	1996-02-15	{"total_dates": 1, "sample_dates": ["1996-02-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
810	120	123	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
811	121	122	traveled_with	1	1996-02-15	1996-02-15	{"total_dates": 1, "sample_dates": ["1996-02-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
812	121	123	traveled_with	2	1996-02-15	1996-02-19	{"total_dates": 2, "sample_dates": ["1996-02-15", "1996-02-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
813	122	123	traveled_with	1	1996-02-15	1996-02-15	{"total_dates": 1, "sample_dates": ["1996-02-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
814	123	129	traveled_with	1	1996-11-11	1996-11-11	{"total_dates": 1, "sample_dates": ["1996-11-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
815	123	149	traveled_with	1	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
816	123	150	traveled_with	1	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
817	123	157	traveled_with	1	1996-11-11	1996-11-11	{"total_dates": 1, "sample_dates": ["1996-11-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
818	123	167	traveled_with	1	1996-11-11	1996-11-11	{"total_dates": 1, "sample_dates": ["1996-11-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
819	123	285	traveled_with	1	2000-09-29	2000-09-29	{"total_dates": 1, "sample_dates": ["2000-09-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
820	127	155	traveled_with	2	1997-09-22	1997-10-17	{"total_dates": 2, "sample_dates": ["1997-09-22", "1997-10-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
821	127	160	traveled_with	1	1998-02-09	1998-02-09	{"total_dates": 1, "sample_dates": ["1998-02-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
822	127	176	traveled_with	2	1997-01-24	1997-01-25	{"total_dates": 2, "sample_dates": ["1997-01-24", "1997-01-25"], "shared_flight_count": 2}	2026-02-05 22:53:03
823	127	203	traveled_with	21	1997-10-17	2000-02-02	{"total_dates": 19, "sample_dates": ["1997-10-17", "1998-02-09", "1998-05-09", "1998-05-11", "1998-05-20", "1998-06-12", "1998-06-15", "1998-11-14", "1999-08-07", "1999-08-14"], "shared_flight_count": 21}	2026-02-05 22:53:03
824	127	209	traveled_with	2	1998-02-09	1999-09-13	{"total_dates": 2, "sample_dates": ["1998-02-09", "1999-09-13"], "shared_flight_count": 2}	2026-02-05 22:53:03
825	127	214	traveled_with	1	1998-05-09	1998-05-09	{"total_dates": 1, "sample_dates": ["1998-05-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
826	127	239	traveled_with	2	1998-05-11	1998-05-20	{"total_dates": 2, "sample_dates": ["1998-05-11", "1998-05-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
827	127	241	traveled_with	2	1998-06-12	1998-06-15	{"total_dates": 2, "sample_dates": ["1998-06-12", "1998-06-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
828	127	247	traveled_with	1	1999-09-07	1999-09-07	{"total_dates": 1, "sample_dates": ["1999-09-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
829	127	256	traveled_with	5	1998-11-14	2000-02-02	{"total_dates": 5, "sample_dates": ["1998-11-14", "1998-11-15", "1998-11-16", "2000-01-31", "2000-02-02"], "shared_flight_count": 5}	2026-02-05 22:53:03
830	127	258	traveled_with	4	1999-05-10	1999-07-04	{"total_dates": 3, "sample_dates": ["1999-05-10", "1999-07-03", "1999-07-04"], "shared_flight_count": 4}	2026-02-05 22:53:03
831	127	260	traveled_with	2	1999-05-10	1999-05-10	{"total_dates": 1, "sample_dates": ["1999-05-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
832	127	269	traveled_with	1	1999-08-07	1999-08-07	{"total_dates": 1, "sample_dates": ["1999-08-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
833	127	270	traveled_with	3	1999-09-02	1999-11-30	{"total_dates": 3, "sample_dates": ["1999-09-02", "1999-09-07", "1999-11-30"], "shared_flight_count": 3}	2026-02-05 22:53:03
834	127	271	traveled_with	1	1999-09-08	1999-09-08	{"total_dates": 1, "sample_dates": ["1999-09-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
835	128	129	traveled_with	1	1996-03-22	1996-03-22	{"total_dates": 1, "sample_dates": ["1996-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
836	129	157	traveled_with	2	1996-11-07	1996-11-11	{"total_dates": 2, "sample_dates": ["1996-11-07", "1996-11-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
837	129	167	traveled_with	2	1996-11-07	1996-11-11	{"total_dates": 2, "sample_dates": ["1996-11-07", "1996-11-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
838	130	162	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
839	130	163	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
840	131	132	traveled_with	2	1996-05-02	1996-05-03	{"total_dates": 2, "sample_dates": ["1996-05-02", "1996-05-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
841	131	133	traveled_with	2	1996-05-02	1996-05-03	{"total_dates": 2, "sample_dates": ["1996-05-02", "1996-05-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
842	131	134	traveled_with	2	1996-05-02	1996-05-03	{"total_dates": 2, "sample_dates": ["1996-05-02", "1996-05-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
843	131	135	traveled_with	1	1996-05-03	1996-05-03	{"total_dates": 1, "sample_dates": ["1996-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
844	131	285	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
845	131	286	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
846	131	287	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
847	131	288	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
848	132	133	traveled_with	2	1996-05-02	1996-05-03	{"total_dates": 2, "sample_dates": ["1996-05-02", "1996-05-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
849	132	134	traveled_with	2	1996-05-02	1996-05-03	{"total_dates": 2, "sample_dates": ["1996-05-02", "1996-05-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
850	132	135	traveled_with	1	1996-05-03	1996-05-03	{"total_dates": 1, "sample_dates": ["1996-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
851	133	134	traveled_with	2	1996-05-02	1996-05-03	{"total_dates": 2, "sample_dates": ["1996-05-02", "1996-05-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
852	133	135	traveled_with	1	1996-05-03	1996-05-03	{"total_dates": 1, "sample_dates": ["1996-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
853	134	135	traveled_with	1	1996-05-03	1996-05-03	{"total_dates": 1, "sample_dates": ["1996-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
854	139	140	traveled_with	2	1996-06-02	1996-06-05	{"total_dates": 2, "sample_dates": ["1996-06-02", "1996-06-05"], "shared_flight_count": 2}	2026-02-05 22:53:03
855	139	141	traveled_with	1	1996-06-02	1996-06-02	{"total_dates": 1, "sample_dates": ["1996-06-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
856	139	142	traveled_with	1	1996-06-05	1996-06-05	{"total_dates": 1, "sample_dates": ["1996-06-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
857	139	152	traveled_with	2	1997-02-21	1997-02-23	{"total_dates": 2, "sample_dates": ["1997-02-21", "1997-02-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
858	139	181	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
859	139	182	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
860	139	183	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
861	140	141	traveled_with	1	1996-06-02	1996-06-02	{"total_dates": 1, "sample_dates": ["1996-06-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
862	140	142	traveled_with	1	1996-06-05	1996-06-05	{"total_dates": 1, "sample_dates": ["1996-06-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
863	144	156	traveled_with	1	1996-10-15	1996-10-15	{"total_dates": 1, "sample_dates": ["1996-10-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
864	144	157	traveled_with	1	1996-10-15	1996-10-15	{"total_dates": 1, "sample_dates": ["1996-10-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
865	146	147	traveled_with	1	1996-08-12	1996-08-12	{"total_dates": 1, "sample_dates": ["1996-08-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
866	146	148	traveled_with	1	1996-08-12	1996-08-12	{"total_dates": 1, "sample_dates": ["1996-08-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
867	147	148	traveled_with	1	1996-08-12	1996-08-12	{"total_dates": 1, "sample_dates": ["1996-08-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
868	147	155	traveled_with	3	1997-04-15	1997-10-21	{"total_dates": 3, "sample_dates": ["1997-04-15", "1997-04-21", "1997-10-21"], "shared_flight_count": 3}	2026-02-05 22:53:03
869	147	187	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
870	147	188	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
871	147	190	traveled_with	1	1997-04-21	1997-04-21	{"total_dates": 1, "sample_dates": ["1997-04-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
872	147	203	traveled_with	1	1997-10-21	1997-10-21	{"total_dates": 1, "sample_dates": ["1997-10-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
873	148	203	traveled_with	1	1999-11-28	1999-11-28	{"total_dates": 1, "sample_dates": ["1999-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
874	149	150	traveled_with	2	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 2}	2026-02-05 22:53:03
875	149	151	traveled_with	1	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
876	150	151	traveled_with	1	1996-08-18	1996-08-18	{"total_dates": 1, "sample_dates": ["1996-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
877	150	155	traveled_with	1	1997-04-17	1997-04-17	{"total_dates": 1, "sample_dates": ["1997-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
878	152	155	traveled_with	3	1997-08-20	1997-11-29	{"total_dates": 3, "sample_dates": ["1997-08-20", "1997-08-23", "1997-11-29"], "shared_flight_count": 3}	2026-02-05 22:53:03
879	152	160	traveled_with	1	1997-02-02	1997-02-02	{"total_dates": 1, "sample_dates": ["1997-02-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
880	152	174	traveled_with	1	1997-01-11	1997-01-11	{"total_dates": 1, "sample_dates": ["1997-01-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
881	152	177	traveled_with	2	1997-01-30	1997-02-02	{"total_dates": 2, "sample_dates": ["1997-01-30", "1997-02-02"], "shared_flight_count": 2}	2026-02-05 22:53:03
882	152	181	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
883	152	182	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
884	152	183	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
885	152	193	traveled_with	1	1997-05-24	1997-05-24	{"total_dates": 1, "sample_dates": ["1997-05-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
886	152	206	traveled_with	1	1997-11-29	1997-11-29	{"total_dates": 1, "sample_dates": ["1997-11-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
887	152	207	traveled_with	1	1997-11-29	1997-11-29	{"total_dates": 1, "sample_dates": ["1997-11-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
888	153	178	traveled_with	1	1997-02-13	1997-02-13	{"total_dates": 1, "sample_dates": ["1997-02-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
889	155	170	traveled_with	1	1996-11-21	1996-11-21	{"total_dates": 1, "sample_dates": ["1996-11-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
890	155	172	traveled_with	1	1996-12-09	1996-12-09	{"total_dates": 1, "sample_dates": ["1996-12-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
891	155	173	traveled_with	1	1996-12-09	1996-12-09	{"total_dates": 1, "sample_dates": ["1996-12-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
892	155	184	traveled_with	2	1997-02-25	1997-04-10	{"total_dates": 2, "sample_dates": ["1997-02-25", "1997-04-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
893	155	187	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
894	155	188	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
895	155	189	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
896	155	190	traveled_with	1	1997-04-21	1997-04-21	{"total_dates": 1, "sample_dates": ["1997-04-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
897	155	192	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
898	155	194	traveled_with	2	1997-09-19	1997-09-20	{"total_dates": 2, "sample_dates": ["1997-09-19", "1997-09-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
899	155	199	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
900	155	200	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
901	155	201	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
902	155	203	traveled_with	2	1997-10-17	1997-10-21	{"total_dates": 2, "sample_dates": ["1997-10-17", "1997-10-21"], "shared_flight_count": 2}	2026-02-05 22:53:03
903	155	206	traveled_with	1	1997-11-29	1997-11-29	{"total_dates": 1, "sample_dates": ["1997-11-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
904	155	207	traveled_with	1	1997-11-29	1997-11-29	{"total_dates": 1, "sample_dates": ["1997-11-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
905	156	157	traveled_with	1	1996-10-15	1996-10-15	{"total_dates": 1, "sample_dates": ["1996-10-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
906	156	168	traveled_with	1	1996-11-15	1996-11-15	{"total_dates": 1, "sample_dates": ["1996-11-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
907	157	167	traveled_with	2	1996-11-07	1996-11-11	{"total_dates": 2, "sample_dates": ["1996-11-07", "1996-11-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
908	158	376	traveled_with	1	2001-10-15	2001-10-15	{"total_dates": 1, "sample_dates": ["2001-10-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
909	160	161	traveled_with	1	1996-10-27	1996-10-27	{"total_dates": 1, "sample_dates": ["1996-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
910	160	177	traveled_with	1	1997-02-02	1997-02-02	{"total_dates": 1, "sample_dates": ["1997-02-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
911	160	186	traveled_with	1	1997-03-24	1997-03-24	{"total_dates": 1, "sample_dates": ["1997-03-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
912	160	203	traveled_with	5	1998-02-09	2001-05-28	{"total_dates": 5, "sample_dates": ["1998-02-09", "1998-02-12", "2000-05-04", "2001-04-17", "2001-05-28"], "shared_flight_count": 5}	2026-02-05 22:53:03
913	160	209	traveled_with	1	1998-02-09	1998-02-09	{"total_dates": 1, "sample_dates": ["1998-02-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
914	160	210	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
915	160	216	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
916	160	218	traveled_with	2	2001-04-17	2001-11-30	{"total_dates": 2, "sample_dates": ["2001-04-17", "2001-11-30"], "shared_flight_count": 2}	2026-02-05 22:53:03
917	160	331	traveled_with	1	2001-04-17	2001-04-17	{"total_dates": 1, "sample_dates": ["2001-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
918	160	341	traveled_with	1	2001-04-17	2001-04-17	{"total_dates": 1, "sample_dates": ["2001-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
919	160	375	traveled_with	1	2001-11-30	2001-11-30	{"total_dates": 1, "sample_dates": ["2001-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
920	160	378	traveled_with	1	2001-11-12	2001-11-12	{"total_dates": 1, "sample_dates": ["2001-11-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
921	162	163	traveled_with	2	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 2}	2026-02-05 22:53:03
922	162	164	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
923	162	165	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
924	162	166	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
925	163	164	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
926	163	165	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
927	163	166	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
928	164	165	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
929	164	166	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
930	165	166	traveled_with	1	1996-10-30	1996-10-30	{"total_dates": 1, "sample_dates": ["1996-10-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
931	172	173	traveled_with	1	1996-12-09	1996-12-09	{"total_dates": 1, "sample_dates": ["1996-12-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
932	179	180	traveled_with	1	1997-02-17	1997-02-17	{"total_dates": 1, "sample_dates": ["1997-02-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
933	179	194	traveled_with	1	1997-06-21	1997-06-21	{"total_dates": 1, "sample_dates": ["1997-06-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
934	181	182	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
935	181	183	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
936	182	183	traveled_with	1	1997-02-23	1997-02-23	{"total_dates": 1, "sample_dates": ["1997-02-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
937	182	217	traveled_with	1	1998-02-18	1998-02-18	{"total_dates": 1, "sample_dates": ["1998-02-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
938	187	188	traveled_with	1	1997-04-15	1997-04-15	{"total_dates": 1, "sample_dates": ["1997-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
939	190	203	traveled_with	2	1999-07-25	2001-09-15	{"total_dates": 2, "sample_dates": ["1999-07-25", "2001-09-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
940	190	375	traveled_with	1	2001-09-15	2001-09-15	{"total_dates": 1, "sample_dates": ["2001-09-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
941	192	195	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
942	192	196	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
943	192	197	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
944	192	198	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
945	192	199	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
946	192	200	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
947	192	201	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
948	194	339	traveled_with	2	2001-04-03	2001-04-03	{"total_dates": 1, "sample_dates": ["2001-04-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
949	195	196	traveled_with	2	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
950	195	197	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
951	195	198	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
952	196	197	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
953	196	198	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
2687	741	39	communicated_with	7	\N	\N	{"a_to_b": 2, "b_to_a": 5, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
954	197	198	traveled_with	1	1997-09-03	1997-09-03	{"total_dates": 1, "sample_dates": ["1997-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
955	199	200	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
956	199	201	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
957	200	201	traveled_with	1	1997-09-26	1997-09-26	{"total_dates": 1, "sample_dates": ["1997-09-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
958	200	203	traveled_with	7	1998-05-18	2001-03-08	{"total_dates": 5, "sample_dates": ["1998-05-18", "1998-05-20", "1998-09-13", "1999-03-31", "2001-03-08"], "shared_flight_count": 7}	2026-02-05 22:53:03
959	200	236	traveled_with	7	1998-09-13	2001-03-08	{"total_dates": 5, "sample_dates": ["1998-09-13", "1999-03-31", "1999-04-02", "1999-09-02", "2001-03-08"], "shared_flight_count": 7}	2026-02-05 22:53:03
960	200	240	traveled_with	2	1998-05-18	1998-05-18	{"total_dates": 1, "sample_dates": ["1998-05-18"], "shared_flight_count": 2}	2026-02-05 22:53:03
961	200	245	traveled_with	2	1999-11-11	1999-11-14	{"total_dates": 2, "sample_dates": ["1999-11-11", "1999-11-14"], "shared_flight_count": 2}	2026-02-05 22:53:03
962	200	247	traveled_with	1	1999-09-02	1999-09-02	{"total_dates": 1, "sample_dates": ["1999-09-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
963	200	256	traveled_with	3	1999-03-31	1999-04-02	{"total_dates": 2, "sample_dates": ["1999-03-31", "1999-04-02"], "shared_flight_count": 3}	2026-02-05 22:53:03
964	200	257	traveled_with	1	1999-09-02	1999-09-02	{"total_dates": 1, "sample_dates": ["1999-09-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
965	200	258	traveled_with	1	1999-09-02	1999-09-02	{"total_dates": 1, "sample_dates": ["1999-09-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
966	200	259	traveled_with	3	1999-03-31	1999-04-02	{"total_dates": 2, "sample_dates": ["1999-03-31", "1999-04-02"], "shared_flight_count": 3}	2026-02-05 22:53:03
967	200	301	traveled_with	1	2001-03-08	2001-03-08	{"total_dates": 1, "sample_dates": ["2001-03-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
968	200	306	traveled_with	1	2001-03-08	2001-03-08	{"total_dates": 1, "sample_dates": ["2001-03-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
969	203	204	traveled_with	2	1997-11-04	1998-02-28	{"total_dates": 2, "sample_dates": ["1997-11-04", "1998-02-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
970	203	205	traveled_with	1	1997-11-04	1997-11-04	{"total_dates": 1, "sample_dates": ["1997-11-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
971	203	209	traveled_with	3	1997-12-17	1998-09-08	{"total_dates": 3, "sample_dates": ["1997-12-17", "1998-02-09", "1998-09-08"], "shared_flight_count": 3}	2026-02-05 22:53:03
972	203	210	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
973	203	211	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
974	203	212	traveled_with	1	1998-01-03	1998-01-03	{"total_dates": 1, "sample_dates": ["1998-01-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
975	203	213	traveled_with	3	1998-01-08	1998-03-27	{"total_dates": 3, "sample_dates": ["1998-01-08", "1998-01-10", "1998-03-27"], "shared_flight_count": 3}	2026-02-05 22:53:03
976	203	214	traveled_with	4	1998-01-20	1998-05-09	{"total_dates": 3, "sample_dates": ["1998-01-20", "1998-01-25", "1998-05-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
977	203	216	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
978	203	218	traveled_with	2	1998-02-28	2001-04-17	{"total_dates": 2, "sample_dates": ["1998-02-28", "2001-04-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
979	203	222	traveled_with	3	1998-08-07	2000-07-04	{"total_dates": 3, "sample_dates": ["1998-08-07", "2000-01-04", "2000-07-04"], "shared_flight_count": 3}	2026-02-05 22:53:03
980	203	235	traveled_with	1	1998-04-24	1998-04-24	{"total_dates": 1, "sample_dates": ["1998-04-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
981	203	236	traveled_with	5	1998-04-24	2001-03-08	{"total_dates": 4, "sample_dates": ["1998-04-24", "1998-09-13", "1999-03-31", "2001-03-08"], "shared_flight_count": 5}	2026-02-05 22:53:03
982	203	237	traveled_with	1	1998-05-03	1998-05-03	{"total_dates": 1, "sample_dates": ["1998-05-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
983	203	239	traveled_with	2	1998-05-11	1998-05-20	{"total_dates": 2, "sample_dates": ["1998-05-11", "1998-05-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
984	203	240	traveled_with	2	1998-05-18	1998-05-18	{"total_dates": 1, "sample_dates": ["1998-05-18"], "shared_flight_count": 2}	2026-02-05 22:53:03
985	203	241	traveled_with	2	1998-06-12	1998-06-15	{"total_dates": 2, "sample_dates": ["1998-06-12", "1998-06-15"], "shared_flight_count": 2}	2026-02-05 22:53:03
986	203	245	traveled_with	9	1999-11-09	2001-07-11	{"total_dates": 8, "sample_dates": ["1999-11-09", "2000-07-19", "2000-10-21", "2000-10-23", "2001-03-05", "2001-03-06", "2001-07-08", "2001-07-11"], "shared_flight_count": 9}	2026-02-05 22:53:03
987	203	247	traveled_with	9	1998-08-03	2001-08-19	{"total_dates": 8, "sample_dates": ["1998-08-03", "1998-08-21", "1998-10-09", "1998-10-12", "1998-11-20", "1999-05-27", "2001-08-16", "2001-08-19"], "shared_flight_count": 9}	2026-02-05 22:53:03
988	203	248	traveled_with	1	1998-08-03	1998-08-03	{"total_dates": 1, "sample_dates": ["1998-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
989	203	251	traveled_with	1	1998-09-19	1998-09-19	{"total_dates": 1, "sample_dates": ["1998-09-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
990	203	252	traveled_with	1	1998-10-04	1998-10-04	{"total_dates": 1, "sample_dates": ["1998-10-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
991	203	253	traveled_with	1	1998-10-04	1998-10-04	{"total_dates": 1, "sample_dates": ["1998-10-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
992	203	256	traveled_with	5	1998-11-14	2000-02-02	{"total_dates": 5, "sample_dates": ["1998-11-14", "1998-11-16", "1999-03-31", "2000-01-31", "2000-02-02"], "shared_flight_count": 5}	2026-02-05 22:53:03
993	203	257	traveled_with	1	1999-06-27	1999-06-27	{"total_dates": 1, "sample_dates": ["1999-06-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
994	203	258	traveled_with	6	1999-05-18	1999-07-01	{"total_dates": 5, "sample_dates": ["1999-05-18", "1999-05-23", "1999-06-04", "1999-06-07", "1999-07-01"], "shared_flight_count": 6}	2026-02-05 22:53:03
995	203	259	traveled_with	1	1999-03-31	1999-03-31	{"total_dates": 1, "sample_dates": ["1999-03-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
996	203	260	traveled_with	2	2001-05-07	2001-05-07	{"total_dates": 1, "sample_dates": ["2001-05-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
997	203	265	traveled_with	1	2000-05-12	2000-05-12	{"total_dates": 1, "sample_dates": ["2000-05-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
998	203	266	traveled_with	2	1999-05-17	1999-05-17	{"total_dates": 1, "sample_dates": ["1999-05-17"], "shared_flight_count": 2}	2026-02-05 22:53:03
999	203	267	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
1000	203	268	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
1001	203	269	traveled_with	2	1999-08-07	1999-08-08	{"total_dates": 2, "sample_dates": ["1999-08-07", "1999-08-08"], "shared_flight_count": 2}	2026-02-05 22:53:03
1002	203	270	traveled_with	2	1999-09-02	1999-11-30	{"total_dates": 2, "sample_dates": ["1999-09-02", "1999-11-30"], "shared_flight_count": 2}	2026-02-05 22:53:03
1003	203	274	traveled_with	2	1999-10-14	1999-10-14	{"total_dates": 1, "sample_dates": ["1999-10-14"], "shared_flight_count": 2}	2026-02-05 22:53:03
1004	203	275	traveled_with	1	1999-10-27	1999-10-27	{"total_dates": 1, "sample_dates": ["1999-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
1005	203	276	traveled_with	1	1999-10-27	1999-10-27	{"total_dates": 1, "sample_dates": ["1999-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
1006	203	277	traveled_with	1	1999-11-22	1999-11-22	{"total_dates": 1, "sample_dates": ["1999-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1007	203	280	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1008	203	281	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1009	203	282	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1010	203	283	traveled_with	1	2000-05-12	2000-05-12	{"total_dates": 1, "sample_dates": ["2000-05-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1011	203	285	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1012	203	289	traveled_with	1	2000-07-19	2000-07-19	{"total_dates": 1, "sample_dates": ["2000-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1013	203	297	traveled_with	6	2000-10-21	2000-12-09	{"total_dates": 4, "sample_dates": ["2000-10-21", "2000-12-05", "2000-12-06", "2000-12-09"], "shared_flight_count": 6}	2026-02-05 22:53:03
1014	203	298	traveled_with	2	2000-09-10	2000-09-12	{"total_dates": 2, "sample_dates": ["2000-09-10", "2000-09-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
1015	203	301	traveled_with	2	2000-10-21	2001-03-08	{"total_dates": 2, "sample_dates": ["2000-10-21", "2001-03-08"], "shared_flight_count": 2}	2026-02-05 22:53:03
1016	203	306	traveled_with	5	2001-03-08	2001-03-27	{"total_dates": 4, "sample_dates": ["2001-03-08", "2001-03-09", "2001-03-11", "2001-03-27"], "shared_flight_count": 5}	2026-02-05 22:53:03
1017	203	331	traveled_with	12	2001-03-27	2001-09-09	{"total_dates": 11, "sample_dates": ["2001-03-27", "2001-04-05", "2001-04-09", "2001-04-17", "2001-04-20", "2001-05-14", "2001-06-01", "2001-08-29", "2001-09-03", "2001-09-06"], "shared_flight_count": 12}	2026-02-05 22:53:03
1018	203	333	traveled_with	4	2001-06-28	2001-09-25	{"total_dates": 2, "sample_dates": ["2001-06-28", "2001-09-25"], "shared_flight_count": 4}	2026-02-05 22:53:03
1019	203	337	traveled_with	1	2001-04-23	2001-04-23	{"total_dates": 1, "sample_dates": ["2001-04-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1020	203	340	traveled_with	2	2001-04-09	2001-04-09	{"total_dates": 1, "sample_dates": ["2001-04-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
1021	203	341	traveled_with	1	2001-04-17	2001-04-17	{"total_dates": 1, "sample_dates": ["2001-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
1022	203	342	traveled_with	2	2001-04-23	2001-04-23	{"total_dates": 1, "sample_dates": ["2001-04-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
1023	203	360	traveled_with	2	2001-07-08	2001-10-26	{"total_dates": 2, "sample_dates": ["2001-07-08", "2001-10-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
1024	203	363	traveled_with	1	2001-08-05	2001-08-05	{"total_dates": 1, "sample_dates": ["2001-08-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1025	203	368	traveled_with	2	2001-08-16	2001-08-19	{"total_dates": 2, "sample_dates": ["2001-08-16", "2001-08-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
1026	203	369	traveled_with	1	2001-08-16	2001-08-16	{"total_dates": 1, "sample_dates": ["2001-08-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1027	203	370	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1028	203	371	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1029	203	372	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1030	203	374	traveled_with	1	2001-09-03	2001-09-03	{"total_dates": 1, "sample_dates": ["2001-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
1031	203	375	traveled_with	1	2001-09-15	2001-09-15	{"total_dates": 1, "sample_dates": ["2001-09-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1032	204	205	traveled_with	1	1997-11-04	1997-11-04	{"total_dates": 1, "sample_dates": ["1997-11-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
1033	204	218	traveled_with	1	1998-02-28	1998-02-28	{"total_dates": 1, "sample_dates": ["1998-02-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1034	206	207	traveled_with	1	1997-11-29	1997-11-29	{"total_dates": 1, "sample_dates": ["1997-11-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1035	208	398	traveled_with	1	2005-11-16	2005-11-16	{"total_dates": 1, "sample_dates": ["2005-11-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1036	208	422	traveled_with	1	2005-11-16	2005-11-16	{"total_dates": 1, "sample_dates": ["2005-11-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1037	209	210	traveled_with	1	1997-12-17	1997-12-17	{"total_dates": 1, "sample_dates": ["1997-12-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
1038	209	258	traveled_with	1	1999-06-09	1999-06-09	{"total_dates": 1, "sample_dates": ["1999-06-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1039	209	277	traveled_with	1	1999-11-19	1999-11-19	{"total_dates": 1, "sample_dates": ["1999-11-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1040	210	216	traveled_with	1	1998-02-12	1998-02-12	{"total_dates": 1, "sample_dates": ["1998-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1041	211	212	traveled_with	2	1998-01-03	2001-01-11	{"total_dates": 2, "sample_dates": ["1998-01-03", "2001-01-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
1042	211	306	traveled_with	1	2001-01-11	2001-01-11	{"total_dates": 1, "sample_dates": ["2001-01-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
1043	212	306	traveled_with	1	2001-01-11	2001-01-11	{"total_dates": 1, "sample_dates": ["2001-01-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
1044	215	250	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1045	215	265	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1046	215	306	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1047	218	331	traveled_with	1	2001-04-17	2001-04-17	{"total_dates": 1, "sample_dates": ["2001-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
1048	218	341	traveled_with	1	2001-04-17	2001-04-17	{"total_dates": 1, "sample_dates": ["2001-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
1049	218	375	traveled_with	1	2001-11-30	2001-11-30	{"total_dates": 1, "sample_dates": ["2001-11-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
1050	218	398	traveled_with	2	2004-03-07	2004-03-11	{"total_dates": 2, "sample_dates": ["2004-03-07", "2004-03-11"], "shared_flight_count": 2}	2026-02-05 22:53:03
1051	218	399	traveled_with	4	2004-03-07	2004-03-11	{"total_dates": 4, "sample_dates": ["2004-03-07", "2004-03-08", "2004-03-09", "2004-03-11"], "shared_flight_count": 4}	2026-02-05 22:53:03
1052	218	401	traveled_with	1	2004-03-11	2004-03-11	{"total_dates": 1, "sample_dates": ["2004-03-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
1053	220	221	traveled_with	1	1998-04-05	1998-04-05	{"total_dates": 1, "sample_dates": ["1998-04-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1054	220	222	traveled_with	1	1998-04-05	1998-04-05	{"total_dates": 1, "sample_dates": ["1998-04-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1055	221	222	traveled_with	1	1998-04-05	1998-04-05	{"total_dates": 1, "sample_dates": ["1998-04-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1056	222	245	traveled_with	1	1998-06-26	1998-06-26	{"total_dates": 1, "sample_dates": ["1998-06-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
1057	222	274	traveled_with	1	1999-10-18	1999-10-18	{"total_dates": 1, "sample_dates": ["1999-10-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1058	224	225	traveled_with	1	1998-04-06	1998-04-06	{"total_dates": 1, "sample_dates": ["1998-04-06"], "shared_flight_count": 1}	2026-02-05 22:53:03
1059	225	360	traveled_with	1	2001-06-15	2001-06-15	{"total_dates": 1, "sample_dates": ["2001-06-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1060	226	227	traveled_with	1	1998-04-09	1998-04-09	{"total_dates": 1, "sample_dates": ["1998-04-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1061	227	238	traveled_with	1	1998-05-05	1998-05-05	{"total_dates": 1, "sample_dates": ["1998-05-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1062	233	234	traveled_with	2	1998-04-20	1998-04-20	{"total_dates": 1, "sample_dates": ["1998-04-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
1063	235	236	traveled_with	1	1998-04-24	1998-04-24	{"total_dates": 1, "sample_dates": ["1998-04-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1064	236	247	traveled_with	1	1999-09-02	1999-09-02	{"total_dates": 1, "sample_dates": ["1999-09-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1065	236	256	traveled_with	3	1999-03-31	1999-04-02	{"total_dates": 2, "sample_dates": ["1999-03-31", "1999-04-02"], "shared_flight_count": 3}	2026-02-05 22:53:03
1066	236	257	traveled_with	1	1999-09-02	1999-09-02	{"total_dates": 1, "sample_dates": ["1999-09-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1067	236	258	traveled_with	1	1999-09-02	1999-09-02	{"total_dates": 1, "sample_dates": ["1999-09-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1068	236	259	traveled_with	3	1999-03-31	1999-04-02	{"total_dates": 2, "sample_dates": ["1999-03-31", "1999-04-02"], "shared_flight_count": 3}	2026-02-05 22:53:03
1069	236	301	traveled_with	1	2001-03-08	2001-03-08	{"total_dates": 1, "sample_dates": ["2001-03-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1070	236	306	traveled_with	1	2001-03-08	2001-03-08	{"total_dates": 1, "sample_dates": ["2001-03-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1071	237	336	traveled_with	1	2001-03-31	2001-03-31	{"total_dates": 1, "sample_dates": ["2001-03-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
1072	237	337	traveled_with	1	2001-03-31	2001-03-31	{"total_dates": 1, "sample_dates": ["2001-03-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
1073	240	257	traveled_with	1	1999-09-05	1999-09-05	{"total_dates": 1, "sample_dates": ["1999-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1074	240	258	traveled_with	1	1999-09-05	1999-09-05	{"total_dates": 1, "sample_dates": ["1999-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1075	242	243	traveled_with	1	1998-06-18	1998-06-18	{"total_dates": 1, "sample_dates": ["1998-06-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1076	242	244	traveled_with	1	1998-06-21	1998-06-21	{"total_dates": 1, "sample_dates": ["1998-06-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
1077	242	245	traveled_with	1	1998-06-21	1998-06-21	{"total_dates": 1, "sample_dates": ["1998-06-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
1078	242	422	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1079	242	424	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1080	242	433	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1081	242	441	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1082	242	442	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1083	244	245	traveled_with	1	1998-06-21	1998-06-21	{"total_dates": 1, "sample_dates": ["1998-06-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
1084	245	246	traveled_with	1	1998-06-23	1998-06-23	{"total_dates": 1, "sample_dates": ["1998-06-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1085	245	257	traveled_with	1	2000-07-19	2000-07-19	{"total_dates": 1, "sample_dates": ["2000-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1086	245	289	traveled_with	1	2000-07-19	2000-07-19	{"total_dates": 1, "sample_dates": ["2000-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1087	245	297	traveled_with	2	2000-10-21	2000-10-21	{"total_dates": 1, "sample_dates": ["2000-10-21"], "shared_flight_count": 2}	2026-02-05 22:53:03
1088	245	301	traveled_with	1	2000-10-21	2000-10-21	{"total_dates": 1, "sample_dates": ["2000-10-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
1089	245	305	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1090	245	360	traveled_with	1	2001-07-08	2001-07-08	{"total_dates": 1, "sample_dates": ["2001-07-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1091	245	387	traveled_with	3	2003-08-10	2004-06-20	{"total_dates": 3, "sample_dates": ["2003-08-10", "2003-10-19", "2004-06-20"], "shared_flight_count": 3}	2026-02-05 22:53:03
1092	245	391	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1093	245	394	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1094	245	395	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1095	245	398	traveled_with	5	2004-06-20	2004-07-04	{"total_dates": 3, "sample_dates": ["2004-06-20", "2004-07-02", "2004-07-04"], "shared_flight_count": 5}	2026-02-05 22:53:03
1096	245	399	traveled_with	1	2004-08-06	2004-08-06	{"total_dates": 1, "sample_dates": ["2004-08-06"], "shared_flight_count": 1}	2026-02-05 22:53:03
1097	245	405	traveled_with	1	2003-10-19	2003-10-19	{"total_dates": 1, "sample_dates": ["2003-10-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1098	245	418	traveled_with	1	2004-02-09	2004-02-09	{"total_dates": 1, "sample_dates": ["2004-02-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1099	245	424	traveled_with	3	2004-02-09	2004-08-06	{"total_dates": 3, "sample_dates": ["2004-02-09", "2004-06-20", "2004-08-06"], "shared_flight_count": 3}	2026-02-05 22:53:03
1100	245	429	traveled_with	2	2004-06-20	2004-08-06	{"total_dates": 2, "sample_dates": ["2004-06-20", "2004-08-06"], "shared_flight_count": 2}	2026-02-05 22:53:03
1101	245	433	traveled_with	2	2004-06-20	2004-08-06	{"total_dates": 2, "sample_dates": ["2004-06-20", "2004-08-06"], "shared_flight_count": 2}	2026-02-05 22:53:03
1102	245	434	traveled_with	4	2004-07-02	2004-07-04	{"total_dates": 2, "sample_dates": ["2004-07-02", "2004-07-04"], "shared_flight_count": 4}	2026-02-05 22:53:03
1103	245	435	traveled_with	4	2004-07-02	2004-07-04	{"total_dates": 2, "sample_dates": ["2004-07-02", "2004-07-04"], "shared_flight_count": 4}	2026-02-05 22:53:03
1104	245	455	traveled_with	1	2005-02-19	2005-02-19	{"total_dates": 1, "sample_dates": ["2005-02-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1105	245	456	traveled_with	1	2005-02-19	2005-02-19	{"total_dates": 1, "sample_dates": ["2005-02-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1106	247	248	traveled_with	1	1998-08-03	1998-08-03	{"total_dates": 1, "sample_dates": ["1998-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
1107	247	257	traveled_with	1	1999-09-02	1999-09-02	{"total_dates": 1, "sample_dates": ["1999-09-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1108	247	258	traveled_with	3	1999-08-23	1999-09-02	{"total_dates": 3, "sample_dates": ["1999-08-23", "1999-08-26", "1999-09-02"], "shared_flight_count": 3}	2026-02-05 22:53:03
1109	247	267	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
1110	247	268	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
1111	247	270	traveled_with	1	1999-09-07	1999-09-07	{"total_dates": 1, "sample_dates": ["1999-09-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
1112	247	368	traveled_with	2	2001-08-16	2001-08-19	{"total_dates": 2, "sample_dates": ["2001-08-16", "2001-08-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
1113	247	369	traveled_with	1	2001-08-16	2001-08-16	{"total_dates": 1, "sample_dates": ["2001-08-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1114	247	370	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1115	247	371	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1116	247	372	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1117	248	422	traveled_with	1	2004-05-15	2004-05-15	{"total_dates": 1, "sample_dates": ["2004-05-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1118	248	424	traveled_with	1	2004-05-15	2004-05-15	{"total_dates": 1, "sample_dates": ["2004-05-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1119	250	265	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1120	250	306	traveled_with	1	2001-03-22	2001-03-22	{"total_dates": 1, "sample_dates": ["2001-03-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1121	251	422	traveled_with	2	2004-04-15	2005-12-21	{"total_dates": 2, "sample_dates": ["2004-04-15", "2005-12-21"], "shared_flight_count": 2}	2026-02-05 22:53:03
1122	251	424	traveled_with	1	2004-04-15	2004-04-15	{"total_dates": 1, "sample_dates": ["2004-04-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1123	251	457	traveled_with	1	2005-09-14	2005-09-14	{"total_dates": 1, "sample_dates": ["2005-09-14"], "shared_flight_count": 1}	2026-02-05 22:53:03
1124	251	472	traveled_with	1	2005-12-21	2005-12-21	{"total_dates": 1, "sample_dates": ["2005-12-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
1125	252	253	traveled_with	1	1998-10-04	1998-10-04	{"total_dates": 1, "sample_dates": ["1998-10-04"], "shared_flight_count": 1}	2026-02-05 22:53:03
1126	254	255	traveled_with	1	1998-10-06	1998-10-06	{"total_dates": 1, "sample_dates": ["1998-10-06"], "shared_flight_count": 1}	2026-02-05 22:53:03
1127	256	259	traveled_with	3	1999-03-31	1999-04-02	{"total_dates": 2, "sample_dates": ["1999-03-31", "1999-04-02"], "shared_flight_count": 3}	2026-02-05 22:53:03
1128	257	258	traveled_with	4	1999-03-29	1999-09-05	{"total_dates": 4, "sample_dates": ["1999-03-29", "1999-05-02", "1999-09-02", "1999-09-05"], "shared_flight_count": 4}	2026-02-05 22:53:03
1129	257	302	traveled_with	2	2000-11-05	2000-11-07	{"total_dates": 2, "sample_dates": ["2000-11-05", "2000-11-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
1130	258	260	traveled_with	2	1999-05-10	1999-05-10	{"total_dates": 1, "sample_dates": ["1999-05-10"], "shared_flight_count": 2}	2026-02-05 22:53:03
1131	258	264	traveled_with	1	1999-04-25	1999-04-25	{"total_dates": 1, "sample_dates": ["1999-04-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1132	258	265	traveled_with	1	1999-04-25	1999-04-25	{"total_dates": 1, "sample_dates": ["1999-04-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1133	260	261	traveled_with	1	1999-04-08	1999-04-08	{"total_dates": 1, "sample_dates": ["1999-04-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1134	260	262	traveled_with	1	1999-04-11	1999-04-11	{"total_dates": 1, "sample_dates": ["1999-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
1135	260	263	traveled_with	1	1999-04-11	1999-04-11	{"total_dates": 1, "sample_dates": ["1999-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
1136	262	263	traveled_with	1	1999-04-11	1999-04-11	{"total_dates": 1, "sample_dates": ["1999-04-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
1137	264	265	traveled_with	1	1999-04-25	1999-04-25	{"total_dates": 1, "sample_dates": ["1999-04-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1138	265	283	traveled_with	1	2000-05-12	2000-05-12	{"total_dates": 1, "sample_dates": ["2000-05-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1139	265	305	traveled_with	3	2001-01-06	2001-03-19	{"total_dates": 3, "sample_dates": ["2001-01-06", "2001-03-16", "2001-03-19"], "shared_flight_count": 3}	2026-02-05 22:53:03
1140	265	306	traveled_with	6	2001-03-15	2001-03-22	{"total_dates": 4, "sample_dates": ["2001-03-15", "2001-03-16", "2001-03-19", "2001-03-22"], "shared_flight_count": 6}	2026-02-05 22:53:03
1141	265	331	traveled_with	6	2001-03-15	2001-03-19	{"total_dates": 3, "sample_dates": ["2001-03-15", "2001-03-16", "2001-03-19"], "shared_flight_count": 6}	2026-02-05 22:53:03
1142	265	332	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1143	265	333	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1144	265	334	traveled_with	1	2001-03-19	2001-03-19	{"total_dates": 1, "sample_dates": ["2001-03-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1145	265	360	traveled_with	1	2001-10-23	2001-10-23	{"total_dates": 1, "sample_dates": ["2001-10-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1146	267	268	traveled_with	1	1999-05-27	1999-05-27	{"total_dates": 1, "sample_dates": ["1999-05-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
1147	275	276	traveled_with	1	1999-10-27	1999-10-27	{"total_dates": 1, "sample_dates": ["1999-10-27"], "shared_flight_count": 1}	2026-02-05 22:53:03
1148	280	281	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1149	280	282	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1150	281	282	traveled_with	1	2000-05-08	2000-05-08	{"total_dates": 1, "sample_dates": ["2000-05-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1151	285	286	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1152	285	287	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1153	285	288	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1154	286	287	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1155	286	288	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1156	287	288	traveled_with	1	2000-06-25	2000-06-25	{"total_dates": 1, "sample_dates": ["2000-06-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1157	297	301	traveled_with	1	2000-10-21	2000-10-21	{"total_dates": 1, "sample_dates": ["2000-10-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
1158	297	303	traveled_with	1	2000-12-07	2000-12-07	{"total_dates": 1, "sample_dates": ["2000-12-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
1159	297	304	traveled_with	1	2000-12-07	2000-12-07	{"total_dates": 1, "sample_dates": ["2000-12-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
1160	301	306	traveled_with	1	2001-03-08	2001-03-08	{"total_dates": 1, "sample_dates": ["2001-03-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1161	303	304	traveled_with	1	2000-12-07	2000-12-07	{"total_dates": 1, "sample_dates": ["2000-12-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
1162	305	306	traveled_with	2	2001-03-16	2001-03-19	{"total_dates": 2, "sample_dates": ["2001-03-16", "2001-03-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
1163	305	331	traveled_with	2	2001-03-16	2001-03-19	{"total_dates": 2, "sample_dates": ["2001-03-16", "2001-03-19"], "shared_flight_count": 2}	2026-02-05 22:53:03
1164	305	333	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1165	305	334	traveled_with	1	2001-03-19	2001-03-19	{"total_dates": 1, "sample_dates": ["2001-03-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1166	305	387	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1167	305	391	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1168	305	394	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1169	305	395	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1170	306	331	traveled_with	6	2001-03-15	2001-03-27	{"total_dates": 4, "sample_dates": ["2001-03-15", "2001-03-16", "2001-03-19", "2001-03-27"], "shared_flight_count": 6}	2026-02-05 22:53:03
1171	306	332	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1172	306	333	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1173	306	334	traveled_with	1	2001-03-19	2001-03-19	{"total_dates": 1, "sample_dates": ["2001-03-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1174	306	415	traveled_with	1	2003-12-07	2003-12-07	{"total_dates": 1, "sample_dates": ["2003-12-07"], "shared_flight_count": 1}	2026-02-05 22:53:03
1175	331	332	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1176	331	333	traveled_with	1	2001-03-16	2001-03-16	{"total_dates": 1, "sample_dates": ["2001-03-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1177	331	334	traveled_with	1	2001-03-19	2001-03-19	{"total_dates": 1, "sample_dates": ["2001-03-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1178	331	336	traveled_with	1	2001-03-29	2001-03-29	{"total_dates": 1, "sample_dates": ["2001-03-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1179	331	337	traveled_with	1	2001-03-29	2001-03-29	{"total_dates": 1, "sample_dates": ["2001-03-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1180	331	340	traveled_with	3	2001-04-09	2001-04-11	{"total_dates": 2, "sample_dates": ["2001-04-09", "2001-04-11"], "shared_flight_count": 3}	2026-02-05 22:53:03
1181	331	341	traveled_with	1	2001-04-17	2001-04-17	{"total_dates": 1, "sample_dates": ["2001-04-17"], "shared_flight_count": 1}	2026-02-05 22:53:03
1182	331	374	traveled_with	1	2001-09-03	2001-09-03	{"total_dates": 1, "sample_dates": ["2001-09-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
1183	336	337	traveled_with	2	2001-03-29	2001-03-31	{"total_dates": 2, "sample_dates": ["2001-03-29", "2001-03-31"], "shared_flight_count": 2}	2026-02-05 22:53:03
1184	337	342	traveled_with	1	2001-04-23	2001-04-23	{"total_dates": 1, "sample_dates": ["2001-04-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1185	355	356	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1186	355	357	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1187	355	358	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1188	355	359	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1189	356	357	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1190	356	358	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1191	356	359	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1192	357	358	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1193	357	359	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1194	358	359	traveled_with	1	2001-06-08	2001-06-08	{"total_dates": 1, "sample_dates": ["2001-06-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1195	361	362	traveled_with	1	2001-06-22	2001-06-22	{"total_dates": 1, "sample_dates": ["2001-06-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1196	361	382	traveled_with	1	2001-12-13	2001-12-13	{"total_dates": 1, "sample_dates": ["2001-12-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1197	361	383	traveled_with	1	2001-12-13	2001-12-13	{"total_dates": 1, "sample_dates": ["2001-12-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1198	361	391	traveled_with	1	2005-11-08	2005-11-08	{"total_dates": 1, "sample_dates": ["2005-11-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1199	361	398	traveled_with	1	2005-11-08	2005-11-08	{"total_dates": 1, "sample_dates": ["2005-11-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1200	361	424	traveled_with	1	2005-11-08	2005-11-08	{"total_dates": 1, "sample_dates": ["2005-11-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1201	361	457	traveled_with	1	2005-11-08	2005-11-08	{"total_dates": 1, "sample_dates": ["2005-11-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1202	361	469	traveled_with	1	2005-11-08	2005-11-08	{"total_dates": 1, "sample_dates": ["2005-11-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1203	368	369	traveled_with	1	2001-08-16	2001-08-16	{"total_dates": 1, "sample_dates": ["2001-08-16"], "shared_flight_count": 1}	2026-02-05 22:53:03
1204	368	370	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1205	368	371	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1206	368	372	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1207	368	384	traveled_with	2	2001-12-26	2001-12-26	{"total_dates": 1, "sample_dates": ["2001-12-26"], "shared_flight_count": 2}	2026-02-05 22:53:03
1208	370	371	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1209	370	372	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1210	371	372	traveled_with	1	2001-08-19	2001-08-19	{"total_dates": 1, "sample_dates": ["2001-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1211	382	383	traveled_with	1	2001-12-13	2001-12-13	{"total_dates": 1, "sample_dates": ["2001-12-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1212	383	387	traveled_with	1	2004-01-23	2004-01-23	{"total_dates": 1, "sample_dates": ["2004-01-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1213	383	391	traveled_with	1	2004-01-23	2004-01-23	{"total_dates": 1, "sample_dates": ["2004-01-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1214	383	398	traveled_with	1	2004-01-23	2004-01-23	{"total_dates": 1, "sample_dates": ["2004-01-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1215	383	399	traveled_with	1	2004-01-23	2004-01-23	{"total_dates": 1, "sample_dates": ["2004-01-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1216	383	422	traveled_with	1	2004-01-23	2004-01-23	{"total_dates": 1, "sample_dates": ["2004-01-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1217	383	424	traveled_with	1	2004-01-23	2004-01-23	{"total_dates": 1, "sample_dates": ["2004-01-23"], "shared_flight_count": 1}	2026-02-05 22:53:03
1218	387	388	traveled_with	6	2003-06-29	2003-09-22	{"total_dates": 6, "sample_dates": ["2003-06-29", "2003-07-02", "2003-07-07", "2003-07-14", "2003-08-31", "2003-09-22"], "shared_flight_count": 6}	2026-02-05 22:53:03
1219	387	389	traveled_with	1	2003-06-29	2003-06-29	{"total_dates": 1, "sample_dates": ["2003-06-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1220	387	390	traveled_with	2	2003-07-02	2003-07-07	{"total_dates": 2, "sample_dates": ["2003-07-02", "2003-07-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
1221	387	391	traveled_with	8	2003-07-14	2004-07-11	{"total_dates": 7, "sample_dates": ["2003-07-14", "2003-07-31", "2003-08-10", "2003-08-13", "2003-11-14", "2004-01-23", "2004-07-11"], "shared_flight_count": 8}	2026-02-05 22:53:03
1222	387	392	traveled_with	1	2003-07-14	2003-07-14	{"total_dates": 1, "sample_dates": ["2003-07-14"], "shared_flight_count": 1}	2026-02-05 22:53:03
1223	387	393	traveled_with	1	2003-07-31	2003-07-31	{"total_dates": 1, "sample_dates": ["2003-07-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
1224	387	394	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1225	387	395	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1226	387	398	traveled_with	18	2003-09-22	2004-07-25	{"total_dates": 18, "sample_dates": ["2003-09-22", "2004-01-20", "2004-01-23", "2004-01-26", "2004-01-28", "2004-02-02", "2004-02-19", "2004-02-22", "2004-04-06", "2004-04-11"], "shared_flight_count": 18}	2026-02-05 22:53:03
1227	387	399	traveled_with	16	2003-09-22	2004-06-15	{"total_dates": 16, "sample_dates": ["2003-09-22", "2003-10-11", "2003-10-26", "2004-01-20", "2004-01-23", "2004-01-26", "2004-01-28", "2004-02-02", "2004-02-19", "2004-02-22"], "shared_flight_count": 16}	2026-02-05 22:53:03
1228	387	404	traveled_with	1	2003-10-11	2003-10-11	{"total_dates": 1, "sample_dates": ["2003-10-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
1229	387	405	traveled_with	1	2003-10-19	2003-10-19	{"total_dates": 1, "sample_dates": ["2003-10-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1230	387	422	traveled_with	14	2004-01-20	2004-07-25	{"total_dates": 14, "sample_dates": ["2004-01-20", "2004-01-23", "2004-01-26", "2004-01-28", "2004-02-02", "2004-02-19", "2004-02-22", "2004-04-06", "2004-04-22", "2004-04-27"], "shared_flight_count": 14}	2026-02-05 22:53:03
1231	387	424	traveled_with	9	2004-01-20	2004-07-22	{"total_dates": 9, "sample_dates": ["2004-01-20", "2004-01-23", "2004-02-19", "2004-02-22", "2004-04-22", "2004-04-27", "2004-06-15", "2004-06-20", "2004-07-22"], "shared_flight_count": 9}	2026-02-05 22:53:03
1232	387	425	traveled_with	2	2004-02-02	2004-02-22	{"total_dates": 2, "sample_dates": ["2004-02-02", "2004-02-22"], "shared_flight_count": 2}	2026-02-05 22:53:03
1233	387	429	traveled_with	1	2004-06-20	2004-06-20	{"total_dates": 1, "sample_dates": ["2004-06-20"], "shared_flight_count": 1}	2026-02-05 22:53:03
1234	387	430	traveled_with	1	2004-04-22	2004-04-22	{"total_dates": 1, "sample_dates": ["2004-04-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1235	387	433	traveled_with	1	2004-06-20	2004-06-20	{"total_dates": 1, "sample_dates": ["2004-06-20"], "shared_flight_count": 1}	2026-02-05 22:53:03
1236	387	439	traveled_with	2	2004-07-22	2004-07-25	{"total_dates": 2, "sample_dates": ["2004-07-22", "2004-07-25"], "shared_flight_count": 2}	2026-02-05 22:53:03
1237	388	389	traveled_with	1	2003-06-29	2003-06-29	{"total_dates": 1, "sample_dates": ["2003-06-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1238	388	390	traveled_with	2	2003-07-02	2003-07-07	{"total_dates": 2, "sample_dates": ["2003-07-02", "2003-07-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
1239	388	391	traveled_with	2	2003-07-11	2003-07-14	{"total_dates": 2, "sample_dates": ["2003-07-11", "2003-07-14"], "shared_flight_count": 2}	2026-02-05 22:53:03
1240	388	392	traveled_with	1	2003-07-14	2003-07-14	{"total_dates": 1, "sample_dates": ["2003-07-14"], "shared_flight_count": 1}	2026-02-05 22:53:03
1241	388	398	traveled_with	4	2003-09-22	2004-12-03	{"total_dates": 4, "sample_dates": ["2003-09-22", "2004-11-23", "2004-11-28", "2004-12-03"], "shared_flight_count": 4}	2026-02-05 22:53:03
1242	388	399	traveled_with	1	2003-09-22	2003-09-22	{"total_dates": 1, "sample_dates": ["2003-09-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1243	388	422	traveled_with	3	2004-11-23	2004-12-03	{"total_dates": 3, "sample_dates": ["2004-11-23", "2004-11-28", "2004-12-03"], "shared_flight_count": 3}	2026-02-05 22:53:03
1244	388	424	traveled_with	3	2004-11-23	2004-12-03	{"total_dates": 3, "sample_dates": ["2004-11-23", "2004-11-28", "2004-12-03"], "shared_flight_count": 3}	2026-02-05 22:53:03
1245	388	442	traveled_with	2	2004-11-23	2004-11-28	{"total_dates": 2, "sample_dates": ["2004-11-23", "2004-11-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
1246	388	450	traveled_with	1	2004-12-03	2004-12-03	{"total_dates": 1, "sample_dates": ["2004-12-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
1247	391	392	traveled_with	1	2003-07-14	2003-07-14	{"total_dates": 1, "sample_dates": ["2003-07-14"], "shared_flight_count": 1}	2026-02-05 22:53:03
1248	391	393	traveled_with	1	2003-07-31	2003-07-31	{"total_dates": 1, "sample_dates": ["2003-07-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
1249	391	394	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1250	391	395	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1251	391	398	traveled_with	6	2004-01-23	2005-11-08	{"total_dates": 6, "sample_dates": ["2004-01-23", "2004-07-11", "2004-11-18", "2005-01-27", "2005-01-31", "2005-11-08"], "shared_flight_count": 6}	2026-02-05 22:53:03
1252	391	399	traveled_with	2	2003-10-01	2004-01-23	{"total_dates": 2, "sample_dates": ["2003-10-01", "2004-01-23"], "shared_flight_count": 2}	2026-02-05 22:53:03
1253	391	400	traveled_with	1	2003-09-30	2003-09-30	{"total_dates": 1, "sample_dates": ["2003-09-30"], "shared_flight_count": 1}	2026-02-05 22:53:03
1254	391	401	traveled_with	1	2003-10-01	2003-10-01	{"total_dates": 1, "sample_dates": ["2003-10-01"], "shared_flight_count": 1}	2026-02-05 22:53:03
1255	391	406	traveled_with	5	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 5}	2026-02-05 22:53:03
1256	391	407	traveled_with	4	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
1257	391	408	traveled_with	2	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
1258	391	409	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1259	391	410	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1260	391	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1261	391	422	traveled_with	7	2004-01-23	2005-01-31	{"total_dates": 6, "sample_dates": ["2004-01-23", "2004-07-11", "2004-11-16", "2004-11-18", "2005-01-27", "2005-01-31"], "shared_flight_count": 7}	2026-02-05 22:53:03
1262	391	424	traveled_with	5	2004-01-23	2005-11-08	{"total_dates": 5, "sample_dates": ["2004-01-23", "2004-11-18", "2005-01-27", "2005-01-31", "2005-11-08"], "shared_flight_count": 5}	2026-02-05 22:53:03
1263	391	442	traveled_with	1	2004-11-18	2004-11-18	{"total_dates": 1, "sample_dates": ["2004-11-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1264	391	452	traveled_with	1	2005-01-31	2005-01-31	{"total_dates": 1, "sample_dates": ["2005-01-31"], "shared_flight_count": 1}	2026-02-05 22:53:03
1265	391	457	traveled_with	1	2005-11-08	2005-11-08	{"total_dates": 1, "sample_dates": ["2005-11-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1266	391	469	traveled_with	1	2005-11-08	2005-11-08	{"total_dates": 1, "sample_dates": ["2005-11-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1267	394	395	traveled_with	1	2003-08-10	2003-08-10	{"total_dates": 1, "sample_dates": ["2003-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1268	398	399	traveled_with	38	2003-09-22	2004-11-14	{"total_dates": 34, "sample_dates": ["2003-09-22", "2003-10-03", "2003-10-06", "2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23", "2004-01-26", "2004-01-28", "2004-02-02"], "shared_flight_count": 38}	2026-02-05 22:53:03
1269	398	401	traveled_with	6	2004-03-03	2005-11-12	{"total_dates": 5, "sample_dates": ["2004-03-03", "2004-03-11", "2004-03-13", "2004-11-14", "2005-11-12"], "shared_flight_count": 6}	2026-02-05 22:53:03
1270	398	416	traveled_with	2	2003-12-07	2003-12-07	{"total_dates": 1, "sample_dates": ["2003-12-07"], "shared_flight_count": 2}	2026-02-05 22:53:03
1271	398	418	traveled_with	4	2004-01-02	2004-07-19	{"total_dates": 4, "sample_dates": ["2004-01-02", "2004-01-12", "2004-07-15", "2004-07-19"], "shared_flight_count": 4}	2026-02-05 22:53:03
1272	398	421	traveled_with	1	2004-01-02	2004-01-02	{"total_dates": 1, "sample_dates": ["2004-01-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1273	398	422	traveled_with	94	2004-01-02	2006-01-16	{"total_dates": 82, "sample_dates": ["2004-01-02", "2004-01-03", "2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23", "2004-01-26", "2004-01-28", "2004-02-02", "2004-02-17"], "shared_flight_count": 94}	2026-02-05 22:53:03
1274	398	423	traveled_with	2	2004-01-03	2004-01-03	{"total_dates": 1, "sample_dates": ["2004-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
1275	398	424	traveled_with	65	2004-01-12	2005-11-20	{"total_dates": 60, "sample_dates": ["2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23", "2004-02-17", "2004-02-19", "2004-02-22", "2004-02-24", "2004-02-27", "2004-02-29"], "shared_flight_count": 65}	2026-02-05 22:53:03
1276	398	425	traveled_with	4	2004-02-02	2004-02-22	{"total_dates": 3, "sample_dates": ["2004-02-02", "2004-02-17", "2004-02-22"], "shared_flight_count": 4}	2026-02-05 22:53:03
1277	398	427	traveled_with	1	2004-02-24	2004-02-24	{"total_dates": 1, "sample_dates": ["2004-02-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1278	398	428	traveled_with	2	2004-03-13	2004-12-21	{"total_dates": 2, "sample_dates": ["2004-03-13", "2004-12-21"], "shared_flight_count": 2}	2026-02-05 22:53:03
1279	398	429	traveled_with	6	2004-06-20	2004-09-16	{"total_dates": 6, "sample_dates": ["2004-06-20", "2004-08-13", "2004-08-18", "2004-08-19", "2004-09-05", "2004-09-16"], "shared_flight_count": 6}	2026-02-05 22:53:03
1280	398	430	traveled_with	1	2004-04-22	2004-04-22	{"total_dates": 1, "sample_dates": ["2004-04-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1281	398	431	traveled_with	1	2004-05-05	2004-05-05	{"total_dates": 1, "sample_dates": ["2004-05-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1282	398	433	traveled_with	2	2004-06-20	2004-09-05	{"total_dates": 2, "sample_dates": ["2004-06-20", "2004-09-05"], "shared_flight_count": 2}	2026-02-05 22:53:03
1283	398	434	traveled_with	4	2004-07-02	2004-07-04	{"total_dates": 2, "sample_dates": ["2004-07-02", "2004-07-04"], "shared_flight_count": 4}	2026-02-05 22:53:03
1284	398	435	traveled_with	5	2004-07-02	2004-08-13	{"total_dates": 3, "sample_dates": ["2004-07-02", "2004-07-04", "2004-08-13"], "shared_flight_count": 5}	2026-02-05 22:53:03
1285	398	436	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1286	398	437	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1287	398	438	traveled_with	1	2004-07-19	2004-07-19	{"total_dates": 1, "sample_dates": ["2004-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1288	398	439	traveled_with	2	2004-07-22	2004-07-25	{"total_dates": 2, "sample_dates": ["2004-07-22", "2004-07-25"], "shared_flight_count": 2}	2026-02-05 22:53:03
1289	398	440	traveled_with	1	2004-08-03	2004-08-03	{"total_dates": 1, "sample_dates": ["2004-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
1290	398	442	traveled_with	18	2004-08-13	2005-05-16	{"total_dates": 16, "sample_dates": ["2004-08-13", "2004-09-16", "2004-10-20", "2004-10-25", "2004-11-18", "2004-11-23", "2004-11-28", "2005-01-01", "2005-01-03", "2005-02-03"], "shared_flight_count": 18}	2026-02-05 22:53:03
1291	398	443	traveled_with	1	2004-08-19	2004-08-19	{"total_dates": 1, "sample_dates": ["2004-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1292	398	446	traveled_with	1	2004-09-05	2004-09-05	{"total_dates": 1, "sample_dates": ["2004-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1293	398	447	traveled_with	1	2004-10-29	2004-10-29	{"total_dates": 1, "sample_dates": ["2004-10-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1294	398	450	traveled_with	7	2004-12-03	2005-11-12	{"total_dates": 7, "sample_dates": ["2004-12-03", "2005-03-01", "2005-05-12", "2005-05-16", "2005-07-10", "2005-08-18", "2005-11-12"], "shared_flight_count": 7}	2026-02-05 22:53:03
1295	398	451	traveled_with	2	2005-01-01	2005-01-01	{"total_dates": 1, "sample_dates": ["2005-01-01"], "shared_flight_count": 2}	2026-02-05 22:53:03
1296	398	452	traveled_with	5	2005-01-31	2005-03-29	{"total_dates": 5, "sample_dates": ["2005-01-31", "2005-02-03", "2005-03-01", "2005-03-24", "2005-03-29"], "shared_flight_count": 5}	2026-02-05 22:53:03
1297	398	457	traveled_with	13	2005-03-24	2005-11-30	{"total_dates": 12, "sample_dates": ["2005-03-24", "2005-03-29", "2005-05-12", "2005-05-16", "2005-07-10", "2005-07-28", "2005-08-01", "2005-09-13", "2005-10-22", "2005-11-08"], "shared_flight_count": 13}	2026-02-05 22:53:03
1298	398	459	traveled_with	2	2005-11-20	2005-11-20	{"total_dates": 1, "sample_dates": ["2005-11-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
1299	398	464	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1300	398	465	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1301	398	467	traveled_with	1	2005-09-25	2005-09-25	{"total_dates": 1, "sample_dates": ["2005-09-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1302	398	469	traveled_with	3	2005-11-08	2006-01-19	{"total_dates": 3, "sample_dates": ["2005-11-08", "2005-11-12", "2006-01-19"], "shared_flight_count": 3}	2026-02-05 22:53:03
1303	398	470	traveled_with	1	2005-11-12	2005-11-12	{"total_dates": 1, "sample_dates": ["2005-11-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1304	399	401	traveled_with	7	2003-10-01	2004-11-14	{"total_dates": 6, "sample_dates": ["2003-10-01", "2004-03-03", "2004-03-11", "2004-03-13", "2004-03-19", "2004-11-14"], "shared_flight_count": 7}	2026-02-05 22:53:03
1305	399	404	traveled_with	1	2003-10-11	2003-10-11	{"total_dates": 1, "sample_dates": ["2003-10-11"], "shared_flight_count": 1}	2026-02-05 22:53:03
1306	399	417	traveled_with	1	2003-12-15	2003-12-15	{"total_dates": 1, "sample_dates": ["2003-12-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1307	399	418	traveled_with	1	2004-01-12	2004-01-12	{"total_dates": 1, "sample_dates": ["2004-01-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1308	399	422	traveled_with	32	2004-01-12	2004-11-14	{"total_dates": 28, "sample_dates": ["2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23", "2004-01-26", "2004-01-28", "2004-02-02", "2004-02-17", "2004-02-19", "2004-02-22"], "shared_flight_count": 32}	2026-02-05 22:53:03
1309	399	424	traveled_with	23	2004-01-12	2004-09-01	{"total_dates": 21, "sample_dates": ["2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23", "2004-02-17", "2004-02-19", "2004-02-22", "2004-02-24", "2004-02-27", "2004-02-29"], "shared_flight_count": 23}	2026-02-05 22:53:03
1310	399	425	traveled_with	4	2004-02-02	2004-02-22	{"total_dates": 3, "sample_dates": ["2004-02-02", "2004-02-17", "2004-02-22"], "shared_flight_count": 4}	2026-02-05 22:53:03
1311	399	427	traveled_with	1	2004-02-24	2004-02-24	{"total_dates": 1, "sample_dates": ["2004-02-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1312	399	428	traveled_with	1	2004-03-13	2004-03-13	{"total_dates": 1, "sample_dates": ["2004-03-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1313	399	429	traveled_with	2	2004-08-06	2004-09-05	{"total_dates": 2, "sample_dates": ["2004-08-06", "2004-09-05"], "shared_flight_count": 2}	2026-02-05 22:53:03
1314	399	430	traveled_with	1	2004-04-22	2004-04-22	{"total_dates": 1, "sample_dates": ["2004-04-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1315	399	433	traveled_with	2	2004-08-06	2004-09-05	{"total_dates": 2, "sample_dates": ["2004-08-06", "2004-09-05"], "shared_flight_count": 2}	2026-02-05 22:53:03
1316	399	440	traveled_with	1	2004-08-03	2004-08-03	{"total_dates": 1, "sample_dates": ["2004-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
1317	399	446	traveled_with	1	2004-09-05	2004-09-05	{"total_dates": 1, "sample_dates": ["2004-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1318	401	422	traveled_with	5	2004-03-03	2005-04-29	{"total_dates": 4, "sample_dates": ["2004-03-03", "2004-03-19", "2004-11-14", "2005-04-29"], "shared_flight_count": 5}	2026-02-05 22:53:03
1319	401	424	traveled_with	1	2004-03-03	2004-03-03	{"total_dates": 1, "sample_dates": ["2004-03-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
1320	401	428	traveled_with	1	2004-03-13	2004-03-13	{"total_dates": 1, "sample_dates": ["2004-03-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1321	401	450	traveled_with	2	2005-04-29	2005-11-12	{"total_dates": 2, "sample_dates": ["2005-04-29", "2005-11-12"], "shared_flight_count": 2}	2026-02-05 22:53:03
1322	401	457	traveled_with	1	2005-11-12	2005-11-12	{"total_dates": 1, "sample_dates": ["2005-11-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1323	401	459	traveled_with	1	2005-04-29	2005-04-29	{"total_dates": 1, "sample_dates": ["2005-04-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1324	401	469	traveled_with	1	2005-11-12	2005-11-12	{"total_dates": 1, "sample_dates": ["2005-11-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1325	401	470	traveled_with	1	2005-11-12	2005-11-12	{"total_dates": 1, "sample_dates": ["2005-11-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1326	406	407	traveled_with	4	2003-11-04	2003-11-09	{"total_dates": 4, "sample_dates": ["2003-11-04", "2003-11-05", "2003-11-06", "2003-11-09"], "shared_flight_count": 4}	2026-02-05 22:53:03
1327	406	408	traveled_with	2	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 2}	2026-02-05 22:53:03
1328	406	409	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1329	406	410	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1330	406	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1331	407	408	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1332	408	409	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1333	408	410	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1334	408	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1335	409	410	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1336	409	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1337	410	411	traveled_with	1	2003-11-09	2003-11-09	{"total_dates": 1, "sample_dates": ["2003-11-09"], "shared_flight_count": 1}	2026-02-05 22:53:03
1338	412	413	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1339	412	414	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1340	413	414	traveled_with	1	2003-11-22	2003-11-22	{"total_dates": 1, "sample_dates": ["2003-11-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1341	418	419	traveled_with	1	2003-12-24	2003-12-24	{"total_dates": 1, "sample_dates": ["2003-12-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1342	418	420	traveled_with	1	2003-12-26	2003-12-26	{"total_dates": 1, "sample_dates": ["2003-12-26"], "shared_flight_count": 1}	2026-02-05 22:53:03
1343	418	421	traveled_with	1	2004-01-02	2004-01-02	{"total_dates": 1, "sample_dates": ["2004-01-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1344	418	422	traveled_with	6	2004-01-02	2004-07-19	{"total_dates": 6, "sample_dates": ["2004-01-02", "2004-01-05", "2004-01-08", "2004-01-12", "2004-07-15", "2004-07-19"], "shared_flight_count": 6}	2026-02-05 22:53:03
1345	418	424	traveled_with	3	2004-01-12	2004-07-19	{"total_dates": 3, "sample_dates": ["2004-01-12", "2004-02-09", "2004-07-19"], "shared_flight_count": 3}	2026-02-05 22:53:03
1346	418	436	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1347	418	437	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1348	418	438	traveled_with	1	2004-07-19	2004-07-19	{"total_dates": 1, "sample_dates": ["2004-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1349	421	422	traveled_with	1	2004-01-02	2004-01-02	{"total_dates": 1, "sample_dates": ["2004-01-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1350	422	423	traveled_with	2	2004-01-03	2004-01-03	{"total_dates": 1, "sample_dates": ["2004-01-03"], "shared_flight_count": 2}	2026-02-05 22:53:03
1351	422	424	traveled_with	75	2004-01-12	2005-11-20	{"total_dates": 69, "sample_dates": ["2004-01-12", "2004-01-16", "2004-01-20", "2004-01-23", "2004-02-12", "2004-02-17", "2004-02-19", "2004-02-22", "2004-02-24", "2004-02-27"], "shared_flight_count": 75}	2026-02-05 22:53:03
1352	422	425	traveled_with	5	2004-02-02	2004-02-22	{"total_dates": 4, "sample_dates": ["2004-02-02", "2004-02-12", "2004-02-17", "2004-02-22"], "shared_flight_count": 5}	2026-02-05 22:53:03
1353	422	426	traveled_with	1	2004-02-12	2004-02-12	{"total_dates": 1, "sample_dates": ["2004-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1354	422	427	traveled_with	1	2004-02-24	2004-02-24	{"total_dates": 1, "sample_dates": ["2004-02-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1355	422	429	traveled_with	5	2004-04-19	2004-09-16	{"total_dates": 5, "sample_dates": ["2004-04-19", "2004-08-13", "2004-08-18", "2004-09-05", "2004-09-16"], "shared_flight_count": 5}	2026-02-05 22:53:03
1356	422	430	traveled_with	1	2004-04-22	2004-04-22	{"total_dates": 1, "sample_dates": ["2004-04-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1357	422	431	traveled_with	1	2004-05-05	2004-05-05	{"total_dates": 1, "sample_dates": ["2004-05-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1358	422	432	traveled_with	1	2004-06-13	2004-06-13	{"total_dates": 1, "sample_dates": ["2004-06-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1359	422	433	traveled_with	2	2004-08-10	2004-09-05	{"total_dates": 2, "sample_dates": ["2004-08-10", "2004-09-05"], "shared_flight_count": 2}	2026-02-05 22:53:03
1360	422	435	traveled_with	1	2004-08-13	2004-08-13	{"total_dates": 1, "sample_dates": ["2004-08-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1361	422	436	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1362	422	437	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1363	422	438	traveled_with	1	2004-07-19	2004-07-19	{"total_dates": 1, "sample_dates": ["2004-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1364	422	439	traveled_with	1	2004-07-25	2004-07-25	{"total_dates": 1, "sample_dates": ["2004-07-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1365	422	440	traveled_with	1	2004-08-03	2004-08-03	{"total_dates": 1, "sample_dates": ["2004-08-03"], "shared_flight_count": 1}	2026-02-05 22:53:03
1366	422	441	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1367	422	442	traveled_with	20	2004-08-10	2005-08-26	{"total_dates": 17, "sample_dates": ["2004-08-10", "2004-08-13", "2004-09-16", "2004-10-20", "2004-11-18", "2004-11-23", "2004-11-28", "2005-01-01", "2005-01-03", "2005-02-03"], "shared_flight_count": 20}	2026-02-05 22:53:03
1368	422	446	traveled_with	1	2004-09-05	2004-09-05	{"total_dates": 1, "sample_dates": ["2004-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1369	422	447	traveled_with	1	2004-10-29	2004-10-29	{"total_dates": 1, "sample_dates": ["2004-10-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1370	422	450	traveled_with	8	2004-12-03	2005-08-18	{"total_dates": 8, "sample_dates": ["2004-12-03", "2005-03-01", "2005-04-06", "2005-04-29", "2005-05-24", "2005-06-01", "2005-07-05", "2005-08-18"], "shared_flight_count": 8}	2026-02-05 22:53:03
1371	422	451	traveled_with	2	2005-01-01	2005-01-01	{"total_dates": 1, "sample_dates": ["2005-01-01"], "shared_flight_count": 2}	2026-02-05 22:53:03
1372	422	452	traveled_with	8	2005-01-06	2005-04-06	{"total_dates": 8, "sample_dates": ["2005-01-06", "2005-01-31", "2005-02-03", "2005-03-01", "2005-03-24", "2005-03-29", "2005-03-31", "2005-04-06"], "shared_flight_count": 8}	2026-02-05 22:53:03
1373	422	457	traveled_with	3	2005-02-24	2005-03-29	{"total_dates": 3, "sample_dates": ["2005-02-24", "2005-03-24", "2005-03-29"], "shared_flight_count": 3}	2026-02-05 22:53:03
1374	422	459	traveled_with	7	2005-04-29	2005-11-20	{"total_dates": 5, "sample_dates": ["2005-04-29", "2005-09-24", "2005-11-02", "2005-11-17", "2005-11-20"], "shared_flight_count": 7}	2026-02-05 22:53:03
1375	422	461	traveled_with	1	2005-09-20	2005-09-20	{"total_dates": 1, "sample_dates": ["2005-09-20"], "shared_flight_count": 1}	2026-02-05 22:53:03
1376	422	462	traveled_with	1	2005-09-24	2005-09-24	{"total_dates": 1, "sample_dates": ["2005-09-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1377	422	464	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1378	422	465	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1379	422	466	traveled_with	1	2005-09-24	2005-09-24	{"total_dates": 1, "sample_dates": ["2005-09-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1380	422	467	traveled_with	1	2005-09-25	2005-09-25	{"total_dates": 1, "sample_dates": ["2005-09-25"], "shared_flight_count": 1}	2026-02-05 22:53:03
1381	422	472	traveled_with	1	2005-12-21	2005-12-21	{"total_dates": 1, "sample_dates": ["2005-12-21"], "shared_flight_count": 1}	2026-02-05 22:53:03
1382	424	425	traveled_with	4	2004-02-12	2004-02-22	{"total_dates": 3, "sample_dates": ["2004-02-12", "2004-02-17", "2004-02-22"], "shared_flight_count": 4}	2026-02-05 22:53:03
1383	424	426	traveled_with	1	2004-02-12	2004-02-12	{"total_dates": 1, "sample_dates": ["2004-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1384	424	427	traveled_with	1	2004-02-24	2004-02-24	{"total_dates": 1, "sample_dates": ["2004-02-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1385	424	429	traveled_with	7	2004-04-19	2004-09-16	{"total_dates": 7, "sample_dates": ["2004-04-19", "2004-06-20", "2004-08-06", "2004-08-13", "2004-08-18", "2004-08-19", "2004-09-16"], "shared_flight_count": 7}	2026-02-05 22:53:03
1386	424	430	traveled_with	1	2004-04-22	2004-04-22	{"total_dates": 1, "sample_dates": ["2004-04-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1387	424	431	traveled_with	1	2004-05-05	2004-05-05	{"total_dates": 1, "sample_dates": ["2004-05-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1388	424	432	traveled_with	1	2004-06-13	2004-06-13	{"total_dates": 1, "sample_dates": ["2004-06-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1389	424	433	traveled_with	3	2004-06-20	2004-08-10	{"total_dates": 3, "sample_dates": ["2004-06-20", "2004-08-06", "2004-08-10"], "shared_flight_count": 3}	2026-02-05 22:53:03
1390	424	435	traveled_with	1	2004-08-13	2004-08-13	{"total_dates": 1, "sample_dates": ["2004-08-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1391	424	438	traveled_with	1	2004-07-19	2004-07-19	{"total_dates": 1, "sample_dates": ["2004-07-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1392	424	439	traveled_with	1	2004-07-22	2004-07-22	{"total_dates": 1, "sample_dates": ["2004-07-22"], "shared_flight_count": 1}	2026-02-05 22:53:03
1393	424	441	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1394	424	442	traveled_with	14	2004-08-10	2005-05-16	{"total_dates": 13, "sample_dates": ["2004-08-10", "2004-08-13", "2004-09-16", "2004-10-20", "2004-11-18", "2004-11-23", "2004-11-28", "2005-02-03", "2005-02-07", "2005-03-01"], "shared_flight_count": 14}	2026-02-05 22:53:03
1395	424	443	traveled_with	1	2004-08-19	2004-08-19	{"total_dates": 1, "sample_dates": ["2004-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1396	424	450	traveled_with	5	2004-12-03	2005-05-16	{"total_dates": 5, "sample_dates": ["2004-12-03", "2005-03-01", "2005-04-06", "2005-05-12", "2005-05-16"], "shared_flight_count": 5}	2026-02-05 22:53:03
1397	424	452	traveled_with	5	2005-01-31	2005-04-06	{"total_dates": 5, "sample_dates": ["2005-01-31", "2005-02-03", "2005-03-01", "2005-03-31", "2005-04-06"], "shared_flight_count": 5}	2026-02-05 22:53:03
1398	424	457	traveled_with	6	2005-02-24	2005-11-28	{"total_dates": 6, "sample_dates": ["2005-02-24", "2005-05-12", "2005-05-16", "2005-10-22", "2005-11-08", "2005-11-28"], "shared_flight_count": 6}	2026-02-05 22:53:03
1399	424	459	traveled_with	3	2005-11-20	2005-11-28	{"total_dates": 2, "sample_dates": ["2005-11-20", "2005-11-28"], "shared_flight_count": 3}	2026-02-05 22:53:03
1400	424	468	traveled_with	1	2005-10-08	2005-10-08	{"total_dates": 1, "sample_dates": ["2005-10-08"], "shared_flight_count": 1}	2026-02-05 22:53:03
1401	424	469	traveled_with	2	2005-11-08	2005-11-28	{"total_dates": 2, "sample_dates": ["2005-11-08", "2005-11-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
1402	424	470	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1403	424	471	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1404	425	426	traveled_with	1	2004-02-12	2004-02-12	{"total_dates": 1, "sample_dates": ["2004-02-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1405	429	433	traveled_with	3	2004-06-20	2004-09-05	{"total_dates": 3, "sample_dates": ["2004-06-20", "2004-08-06", "2004-09-05"], "shared_flight_count": 3}	2026-02-05 22:53:03
1406	429	435	traveled_with	1	2004-08-13	2004-08-13	{"total_dates": 1, "sample_dates": ["2004-08-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1407	429	442	traveled_with	2	2004-08-13	2004-09-16	{"total_dates": 2, "sample_dates": ["2004-08-13", "2004-09-16"], "shared_flight_count": 2}	2026-02-05 22:53:03
1408	429	443	traveled_with	1	2004-08-19	2004-08-19	{"total_dates": 1, "sample_dates": ["2004-08-19"], "shared_flight_count": 1}	2026-02-05 22:53:03
1409	429	446	traveled_with	1	2004-09-05	2004-09-05	{"total_dates": 1, "sample_dates": ["2004-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1410	433	441	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1411	433	442	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1412	433	446	traveled_with	1	2004-09-05	2004-09-05	{"total_dates": 1, "sample_dates": ["2004-09-05"], "shared_flight_count": 1}	2026-02-05 22:53:03
1413	434	435	traveled_with	4	2004-07-02	2004-07-04	{"total_dates": 2, "sample_dates": ["2004-07-02", "2004-07-04"], "shared_flight_count": 4}	2026-02-05 22:53:03
1414	435	442	traveled_with	1	2004-08-13	2004-08-13	{"total_dates": 1, "sample_dates": ["2004-08-13"], "shared_flight_count": 1}	2026-02-05 22:53:03
1415	436	437	traveled_with	1	2004-07-15	2004-07-15	{"total_dates": 1, "sample_dates": ["2004-07-15"], "shared_flight_count": 1}	2026-02-05 22:53:03
1416	441	442	traveled_with	1	2004-08-10	2004-08-10	{"total_dates": 1, "sample_dates": ["2004-08-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1417	442	450	traveled_with	4	2005-03-01	2005-05-16	{"total_dates": 4, "sample_dates": ["2005-03-01", "2005-04-06", "2005-05-12", "2005-05-16"], "shared_flight_count": 4}	2026-02-05 22:53:03
1418	442	451	traveled_with	2	2005-01-01	2005-01-01	{"total_dates": 1, "sample_dates": ["2005-01-01"], "shared_flight_count": 2}	2026-02-05 22:53:03
1419	442	452	traveled_with	5	2005-02-03	2005-04-06	{"total_dates": 5, "sample_dates": ["2005-02-03", "2005-03-01", "2005-03-24", "2005-03-29", "2005-04-06"], "shared_flight_count": 5}	2026-02-05 22:53:03
1420	442	457	traveled_with	4	2005-03-24	2005-05-16	{"total_dates": 4, "sample_dates": ["2005-03-24", "2005-03-29", "2005-05-12", "2005-05-16"], "shared_flight_count": 4}	2026-02-05 22:53:03
1421	444	445	traveled_with	1	2004-09-02	2004-09-02	{"total_dates": 1, "sample_dates": ["2004-09-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1422	450	452	traveled_with	2	2005-03-01	2005-04-06	{"total_dates": 2, "sample_dates": ["2005-03-01", "2005-04-06"], "shared_flight_count": 2}	2026-02-05 22:53:03
1423	450	457	traveled_with	4	2005-05-12	2005-11-12	{"total_dates": 4, "sample_dates": ["2005-05-12", "2005-05-16", "2005-07-10", "2005-11-12"], "shared_flight_count": 4}	2026-02-05 22:53:03
1424	450	459	traveled_with	1	2005-04-29	2005-04-29	{"total_dates": 1, "sample_dates": ["2005-04-29"], "shared_flight_count": 1}	2026-02-05 22:53:03
1425	450	464	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1426	450	465	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1427	450	469	traveled_with	1	2005-11-12	2005-11-12	{"total_dates": 1, "sample_dates": ["2005-11-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1428	450	470	traveled_with	1	2005-11-12	2005-11-12	{"total_dates": 1, "sample_dates": ["2005-11-12"], "shared_flight_count": 1}	2026-02-05 22:53:03
1429	452	457	traveled_with	2	2005-03-24	2005-03-29	{"total_dates": 2, "sample_dates": ["2005-03-24", "2005-03-29"], "shared_flight_count": 2}	2026-02-05 22:53:03
1430	453	454	traveled_with	1	2005-02-10	2005-02-10	{"total_dates": 1, "sample_dates": ["2005-02-10"], "shared_flight_count": 1}	2026-02-05 22:53:03
1431	457	459	traveled_with	4	2005-07-22	2005-11-28	{"total_dates": 4, "sample_dates": ["2005-07-22", "2005-07-25", "2005-08-02", "2005-11-28"], "shared_flight_count": 4}	2026-02-05 22:53:03
1432	457	462	traveled_with	1	2005-08-02	2005-08-02	{"total_dates": 1, "sample_dates": ["2005-08-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1433	457	463	traveled_with	1	2005-08-02	2005-08-02	{"total_dates": 1, "sample_dates": ["2005-08-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1434	457	469	traveled_with	3	2005-11-08	2005-11-28	{"total_dates": 3, "sample_dates": ["2005-11-08", "2005-11-12", "2005-11-28"], "shared_flight_count": 3}	2026-02-05 22:53:03
1435	457	470	traveled_with	2	2005-11-12	2005-11-28	{"total_dates": 2, "sample_dates": ["2005-11-12", "2005-11-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
1436	457	471	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1437	459	462	traveled_with	2	2005-08-02	2005-09-24	{"total_dates": 2, "sample_dates": ["2005-08-02", "2005-09-24"], "shared_flight_count": 2}	2026-02-05 22:53:03
1438	459	463	traveled_with	1	2005-08-02	2005-08-02	{"total_dates": 1, "sample_dates": ["2005-08-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1439	459	466	traveled_with	1	2005-09-24	2005-09-24	{"total_dates": 1, "sample_dates": ["2005-09-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1440	459	469	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1441	459	470	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1442	459	471	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1443	460	461	traveled_with	2	2005-07-20	2005-07-20	{"total_dates": 1, "sample_dates": ["2005-07-20"], "shared_flight_count": 2}	2026-02-05 22:53:03
1444	462	463	traveled_with	1	2005-08-02	2005-08-02	{"total_dates": 1, "sample_dates": ["2005-08-02"], "shared_flight_count": 1}	2026-02-05 22:53:03
1445	462	466	traveled_with	1	2005-09-24	2005-09-24	{"total_dates": 1, "sample_dates": ["2005-09-24"], "shared_flight_count": 1}	2026-02-05 22:53:03
1446	464	465	traveled_with	1	2005-08-18	2005-08-18	{"total_dates": 1, "sample_dates": ["2005-08-18"], "shared_flight_count": 1}	2026-02-05 22:53:03
1447	469	470	traveled_with	2	2005-11-12	2005-11-28	{"total_dates": 2, "sample_dates": ["2005-11-12", "2005-11-28"], "shared_flight_count": 2}	2026-02-05 22:53:03
1448	469	471	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1449	470	471	traveled_with	1	2005-11-28	2005-11-28	{"total_dates": 1, "sample_dates": ["2005-11-28"], "shared_flight_count": 1}	2026-02-05 22:53:03
1450	1	3	paid_by	1	2012-01-01	2012-01-01	{"memo": "Tax advisory services (claimed)", "notes": "Source: EFTA02731023 (Senate Finance Committee Letter). Tax savings achieved: $1B+ in gift/estate taxes. Black refused to answer questions.", "amount": 158000000.0, "purpose": "Payments from Leon Black to Epstein (2012-2017) - no written contract for over $100M", "currency": "USD", "suspicious": true, "transaction_id": 1, "transaction_type": "fee"}	2026-02-05 22:53:03
1451	1	12	communicated_with	3	2009-07-02	2009-07-02	{"sample_dates": ["2009-07-02"], "communication_count": 3, "communication_types": ["email"]}	2026-02-05 22:53:03
1452	1	2	communicated_with	5	\N	\N	{"communication_count": 5, "communication_types": ["email"]}	2026-02-05 22:53:03
1453	1	3	communicated_with	8	\N	\N	{"communication_count": 8, "communication_types": ["email"]}	2026-02-05 22:53:03
1454	4	6	communicated_with	1	\N	\N	{"communication_count": 1, "communication_types": ["email"]}	2026-02-05 22:53:03
1455	1	6	communicated_with	3	\N	\N	{"communication_count": 3, "communication_types": ["email"]}	2026-02-05 22:53:03
1456	1	19	communicated_with	1	\N	\N	{"communication_count": 1, "communication_types": ["email"]}	2026-02-05 22:53:03
1457	13	29	communicated_with	1	\N	\N	{"communication_count": 1, "communication_types": ["email"]}	2026-02-05 22:53:03
1458	85	1	victim_of	1	\N	\N	{"vpl_id": 1, "abuse_type": "sexual_assault", "date_range": "2000-2002", "corroborated": true, "legal_outcome": "Charged in SDNY 2019; died in custody Aug 2019", "corroboration_details": "Multiple victim testimonies, flight logs, financial records. Source: EFTA02731082"}	2026-02-05 22:53:03
1459	85	2	victim_of	1	\N	\N	{"vpl_id": 2, "abuse_type": "trafficking", "date_range": "2000-2002", "corroborated": true, "legal_outcome": "Convicted Dec 2021 on sex trafficking charges", "corroboration_details": "Multiple victim testimonies, proffer admission. Source: Maxwell Proffer, EFTA02731082"}	2026-02-05 22:53:03
1460	85	2	victim_of	1	\N	\N	{"vpl_id": 3, "abuse_type": "recruitment", "date_range": "2000-2002", "corroborated": true, "legal_outcome": "Convicted Dec 2021", "corroboration_details": "Maxwell recruited Giuffre at Mar-a-Lago. Source: victim testimony"}	2026-02-05 22:53:03
1461	473	3	victim_of	1	\N	\N	{"notes": "Victim: 'Black began initiating sexual contact' during massage at Epstein's NYC residence. Another victim provided oral sex.", "vpl_id": 4, "abuse_type": "sexual_contact", "legal_outcome": "No criminal charges", "public_denial": true, "denial_details": "Black has publicly denied allegations", "corroboration_details": "Single victim testimony. Source: EFTA02731082 pg 33"}	2026-02-05 22:53:03
1462	473	4	victim_of	1	\N	\N	{"notes": "Victim: 'he forced [her] to touch his genitals and then raped [her]'. Epstein said he left it to them to decide.", "vpl_id": 5, "abuse_type": "rape", "corroborated": true, "legal_outcome": "No criminal charges; dismissed from Barclays", "public_denial": true, "denial_details": "Staley denied inappropriate relationship", "corroboration_details": "Victim testimony CORROBORATED BY MESSAGES between Staley and Epstein (fn 61). Source: EFTA02731082 pg 33"}	2026-02-05 22:53:03
1463	85	6	victim_of	1	\N	\N	{"notes": "Maxwell told victim to 'make him happy and do the exact same things for him that she did for Epstein'", "vpl_id": 6, "abuse_type": "sexual_assault", "date_range": "2001", "legal_outcome": "Civil settlement ($12M+); no criminal charges", "public_denial": true, "denial_details": "Andrew denied all allegations; settled civil case for $12M+", "corroboration_details": "Single victim testimony. Source: EFTA02731082 pg 58"}	2026-02-05 22:53:03
1464	85	8	victim_of	1	\N	\N	{"notes": "Maxwell told victim 'she had to do to Glen what [she] did for Epstein' meaning sex acts", "vpl_id": 7, "abuse_type": "sexual_contact", "legal_outcome": "No criminal charges", "public_denial": true, "denial_details": "Dubin denied allegations", "corroboration_details": "Single victim testimony. Source: EFTA02731082 pg 58"}	2026-02-05 22:53:03
1465	473	15	victim_of	1	\N	\N	{"notes": "Victim asked to massage Weinstein; 'Weinstein directed [her] to remove her shirt'", "vpl_id": 8, "abuse_type": "sexual_contact", "legal_outcome": "Convicted (separate cases in NY and LA)", "corroboration_details": "Single victim testimony. Source: EFTA02731082 pg 59"}	2026-02-05 22:53:03
1466	473	9	victim_of	1	\N	\N	{"vpl_id": 9, "abuse_type": "trafficking", "date_range": "1990s-2000s", "corroborated": true, "legal_outcome": "Charged in France 2020; died Feb 2022 (suicide in prison)", "corroboration_details": "Multiple sources. Model agent who recruited victims through MC2 agency."}	2026-02-05 22:53:03
1467	473	10	victim_of	1	\N	\N	{"notes": "Scheduled appointments, facilitated access to victims for Epstein", "vpl_id": 10, "abuse_type": "coercion", "corroborated": true, "legal_outcome": "Non-prosecution agreement", "corroboration_details": "Multiple victim testimonies. Source: EFTA02731082"}	2026-02-05 22:53:03
1468	473	11	victim_of	1	\N	\N	{"notes": "Participated in abuse as directed by Epstein; also described as a victim herself", "vpl_id": 11, "abuse_type": "sexual_contact", "corroborated": true, "legal_outcome": "Non-prosecution agreement", "corroboration_details": "Multiple victim testimonies. Source: EFTA02731082"}	2026-02-05 22:53:03
1495	50	1	employed_by	1	\N	\N	{"notes": "Alessi was Epstein's house manager at Palm Beach residence", "original_type": "employer_employee", "evidence_relationship_id": 25}	2026-02-05 22:53:03
1469	473	1	victim_of	1	\N	\N	{"notes": "Systematic trafficking operation using 'lending out' system. Victims began using drugs due to frequency.", "vpl_id": 12, "abuse_type": "trafficking", "date_range": "1990s-2019", "corroborated": true, "legal_outcome": "Charged SDNY 2019; NPA in 2008 (Palm Beach); died Aug 2019", "corroboration_details": "Dozens of victims, consistent testimony, documentary evidence. Source: EFTA02731082, VI Exhibit 1"}	2026-02-05 22:53:03
1470	473	1	victim_of	1	\N	\N	{"notes": "Epstein instructed participant-witnesses to destroy evidence and paid large sums to witnesses", "vpl_id": 13, "abuse_type": "coercion", "corroborated": true, "legal_outcome": "Part of overall criminal enterprise", "corroboration_details": "Documentary evidence. Source: VI Exhibit 1 pg 41"}	2026-02-05 22:53:03
1471	1	2	associated_with	182	\N	\N	{"notes": "Maxwell was Epstein's primary co-conspirator, recruiter, and enabler", "original_type": "co_conspirator", "evidence_relationship_id": 1}	2026-02-05 22:53:03
1472	1	3	associated_with	816	\N	\N	{"efta": "EFTA01660636", "notes": "Black paid Epstein $158M (2012-2017) for tax advisory. Source: EFTA02731023", "detail": "Named in FBI PROMINENT NAMES briefing; multiple victim allegations of sexual assault and trafficking; also alleged present during abuses with Barr", "source": "ds10_fbi_prominent_names", "evidence_type": "corroborated_testimony", "original_type": "business_partner", "ds10_mention_count": 801, "evidence_relationship_id": 2}	2026-02-05 22:53:03
1473	1	4	associated_with	72	\N	\N	{"efta": "EFTA01660636", "notes": "Staley visited Epstein residence; messages exchanged. Source: EFTA02731082", "detail": "Named in FBI PROMINENT NAMES briefing; victim allegation of forced sexual assault during massage", "source": "ds10_fbi_prominent_names", "evidence_type": "single_testimony", "original_type": "friend", "ds10_mention_count": 57, "evidence_relationship_id": 3}	2026-02-05 22:53:03
1474	1	5	associated_with	41	\N	\N	{"efta": "EFTA01660636", "notes": "Wexner was Epstein's primary benefactor and business relationship", "detail": "Named in FBI PROMINENT NAMES briefing; victim allegation of financial/personal relationship", "source": "ds10_fbi_prominent_names", "evidence_type": "single_testimony", "original_type": "business_partner", "ds10_mention_count": 36, "evidence_relationship_id": 4}	2026-02-05 22:53:03
1475	1	6	associated_with	181	\N	\N	{"efta": "EFTA01660636", "notes": "Andrew described as 'good friend of Maxwell's'. Source: EFTA02731082", "detail": "Named in FBI PROMINENT NAMES briefing; multiple allegations including witness corroboration", "source": "ds10_fbi_prominent_names", "evidence_type": "corroborated_testimony", "original_type": "friend", "ds10_mention_count": 166, "evidence_relationship_id": 5}	2026-02-05 22:53:03
1476	1	7	represented_by	1	\N	\N	{"notes": "Dershowitz served as Epstein's defense attorney", "original_type": "attorney_client", "evidence_relationship_id": 6}	2026-02-05 22:53:03
1477	1	8	associated_with	3	\N	\N	{"notes": "Dubin associated with Epstein; victim 'lent out' to Dubin. Source: EFTA02731082", "original_type": "friend", "evidence_relationship_id": 7}	2026-02-05 22:53:03
1478	1	15	associated_with	2	\N	\N	{"efta": "EFTA01660636", "notes": "Victim sent to massage Weinstein at Epstein's direction. Source: EFTA02731082", "detail": "Named in FBI PROMINENT NAMES briefing; multiple victim allegations of massage coercion and sexual assault", "source": "ds10_fbi_prominent_names", "evidence_type": "corroborated_testimony", "original_type": "friend", "ds10_mention_count": 0, "evidence_relationship_id": 8}	2026-02-05 22:53:03
1479	1	9	associated_with	1	\N	\N	{"notes": "Brunel recruited young models for Epstein through MC2 modeling agency", "original_type": "co_conspirator", "evidence_relationship_id": 9}	2026-02-05 22:53:03
1480	1	10	employed_by	1	\N	\N	{"notes": "Kellen scheduled appointments, facilitated access. Non-prosecution agreement", "original_type": "employer_employee", "evidence_relationship_id": 10}	2026-02-05 22:53:03
1481	1	11	employed_by	1	\N	\N	{"notes": "Marcinkova participated in abuse directed by Epstein. Non-prosecution agreement", "original_type": "employer_employee", "evidence_relationship_id": 11}	2026-02-05 22:53:03
1482	1	12	employed_by	1	\N	\N	{"notes": "Groff was executive assistant, facilitated travel. Non-prosecution agreement", "original_type": "employer_employee", "evidence_relationship_id": 12}	2026-02-05 22:53:03
1483	1	28	represented_by	1	\N	\N	{"notes": "Indyke was estate executor and signatory on suspicious accounts. Source: VI Exhibit 1", "original_type": "attorney_client", "evidence_relationship_id": 13}	2026-02-05 22:53:03
1484	1	29	represented_by	1	\N	\N	{"notes": "Kahn was estate executor and signatory on suspicious accounts. Source: VI Exhibit 1", "original_type": "attorney_client", "evidence_relationship_id": 14}	2026-02-05 22:53:03
1485	1	13	associated_with	45	\N	\N	{"efta": "EFTA01660636", "notes": "Clinton flew on Epstein's aircraft multiple times per flight logs", "detail": "Named in FBI PROMINENT NAMES briefing; FBI noted not a victim in case; allegation of orgy invitation (not attended)", "source": "ds10_fbi_prominent_names", "evidence_type": "single_testimony", "original_type": "friend", "ds10_mention_count": 32, "evidence_relationship_id": 15}	2026-02-05 22:53:03
1486	1	14	associated_with	33	\N	\N	{"efta": "EFTA01660636", "notes": "Trump mentioned in Epstein documents", "detail": "Named in FBI PROMINENT NAMES briefing; victim allegations of sexual abuse", "source": "ds10_fbi_prominent_names", "evidence_type": "single_testimony", "original_type": "friend", "ds10_mention_count": 16, "evidence_relationship_id": 16}	2026-02-05 22:53:03
1487	1	77	associated_with	2	\N	\N	{"notes": "Gates mentioned in Epstein documents", "original_type": "friend", "evidence_relationship_id": 17}	2026-02-05 22:53:03
1488	2	6	associated_with	1	\N	\N	{"notes": "Maxwell told victim Andrew was 'a good friend of Maxwell's'. Source: EFTA02731082", "original_type": "friend", "evidence_relationship_id": 18}	2026-02-05 22:53:03
1489	2	8	associated_with	1	\N	\N	{"notes": "Maxwell directed victim to Dubin. Source: EFTA02731082", "original_type": "friend", "evidence_relationship_id": 19}	2026-02-05 22:53:03
1490	2	9	associated_with	1	\N	\N	{"notes": "Brunel and Maxwell collaborated in recruitment", "original_type": "co_conspirator", "evidence_relationship_id": 20}	2026-02-05 22:53:03
1491	2	10	associated_with	1	\N	\N	{"notes": "Kellen worked under Maxwell's direction", "original_type": "co_conspirator", "evidence_relationship_id": 21}	2026-02-05 22:53:03
1492	2	85	recruited_by	1	\N	\N	{"notes": "Maxwell recruited Virginia Giuffre. Source: victim testimony", "original_type": "recruiter_victim", "evidence_relationship_id": 22}	2026-02-05 22:53:03
1493	9	85	associated_with	1	\N	\N	{"notes": "Brunel's MC2 agency involved in recruitment operations", "original_type": "other", "evidence_relationship_id": 23}	2026-02-05 22:53:03
1496	1	81	associated_with	65	\N	\N	{"notes": "Co-appeared on 34 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 26}	2026-02-05 22:53:03
1497	1	107	associated_with	30	\N	\N	{"notes": "Co-appeared on 34 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 27}	2026-02-05 22:53:03
1498	8	81	associated_with	1	\N	\N	{"notes": "Co-appeared on 18 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 28}	2026-02-05 22:53:03
1499	81	107	associated_with	1	\N	\N	{"notes": "Co-appeared on 34 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 29}	2026-02-05 22:53:03
1500	2	81	associated_with	1	\N	\N	{"notes": "Co-appeared on 23 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 30}	2026-02-05 22:53:03
1501	2	107	associated_with	1	\N	\N	{"notes": "Co-appeared on 23 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 31}	2026-02-05 22:53:03
1502	2	109	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 32}	2026-02-05 22:53:03
1503	1	112	associated_with	1	\N	\N	{"notes": "Co-appeared on 28 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 33}	2026-02-05 22:53:03
1504	1	113	associated_with	1	\N	\N	{"notes": "Co-appeared on 27 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 34}	2026-02-05 22:53:03
1505	2	113	associated_with	1	\N	\N	{"notes": "Co-appeared on 14 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 35}	2026-02-05 22:53:03
1506	1	117	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 36}	2026-02-05 22:53:03
1507	2	117	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 37}	2026-02-05 22:53:03
1508	112	118	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 38}	2026-02-05 22:53:03
1509	112	119	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 39}	2026-02-05 22:53:03
1510	112	120	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 40}	2026-02-05 22:53:03
1511	112	121	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 41}	2026-02-05 22:53:03
1512	112	123	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 42}	2026-02-05 22:53:03
1513	118	119	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 43}	2026-02-05 22:53:03
1514	118	120	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 44}	2026-02-05 22:53:03
1515	118	121	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 45}	2026-02-05 22:53:03
1516	118	123	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 46}	2026-02-05 22:53:03
1517	119	120	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 47}	2026-02-05 22:53:03
1518	119	121	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 48}	2026-02-05 22:53:03
1519	119	123	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 49}	2026-02-05 22:53:03
1520	120	121	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 50}	2026-02-05 22:53:03
1521	120	123	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 51}	2026-02-05 22:53:03
1522	121	123	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 52}	2026-02-05 22:53:03
1523	2	112	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 53}	2026-02-05 22:53:03
1524	1	127	associated_with	1	\N	\N	{"notes": "Co-appeared on 37 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 54}	2026-02-05 22:53:03
1525	2	127	associated_with	1	\N	\N	{"notes": "Co-appeared on 30 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 55}	2026-02-05 22:53:03
1526	1	129	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 56}	2026-02-05 22:53:03
1527	107	112	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 57}	2026-02-05 22:53:03
1528	107	129	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 58}	2026-02-05 22:53:03
1529	1	130	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 59}	2026-02-05 22:53:03
1530	131	132	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 60}	2026-02-05 22:53:03
1531	131	133	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 61}	2026-02-05 22:53:03
1532	131	134	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 62}	2026-02-05 22:53:03
1533	132	133	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 63}	2026-02-05 22:53:03
1534	132	134	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 64}	2026-02-05 22:53:03
1535	133	134	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 65}	2026-02-05 22:53:03
1536	1	136	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 66}	2026-02-05 22:53:03
1537	1	137	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 67}	2026-02-05 22:53:03
1538	2	137	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 68}	2026-02-05 22:53:03
1539	1	139	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 69}	2026-02-05 22:53:03
1540	1	140	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 70}	2026-02-05 22:53:03
1541	139	140	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 71}	2026-02-05 22:53:03
1542	1	144	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 72}	2026-02-05 22:53:03
1543	1	147	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 73}	2026-02-05 22:53:03
1544	1	148	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 74}	2026-02-05 22:53:03
1545	2	147	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 75}	2026-02-05 22:53:03
1546	2	148	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 76}	2026-02-05 22:53:03
1547	1	149	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 77}	2026-02-05 22:53:03
1548	1	150	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 78}	2026-02-05 22:53:03
1549	2	150	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 79}	2026-02-05 22:53:03
1550	149	150	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 80}	2026-02-05 22:53:03
1551	1	123	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 81}	2026-02-05 22:53:03
1552	1	152	associated_with	1	\N	\N	{"notes": "Co-appeared on 18 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 82}	2026-02-05 22:53:03
1553	1	153	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 83}	2026-02-05 22:53:03
1554	2	153	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 84}	2026-02-05 22:53:03
1555	1	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 32 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 85}	2026-02-05 22:53:03
1556	2	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 22 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 86}	2026-02-05 22:53:03
1557	1	156	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 87}	2026-02-05 22:53:03
1558	1	157	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 88}	2026-02-05 22:53:03
1559	1	158	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 89}	2026-02-05 22:53:03
1560	2	158	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 90}	2026-02-05 22:53:03
1561	1	160	associated_with	1	\N	\N	{"notes": "Co-appeared on 10 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 91}	2026-02-05 22:53:03
1562	2	160	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 92}	2026-02-05 22:53:03
1563	1	162	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 93}	2026-02-05 22:53:03
1564	1	163	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 94}	2026-02-05 22:53:03
1565	162	163	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 95}	2026-02-05 22:53:03
1566	1	167	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 96}	2026-02-05 22:53:03
1567	8	157	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 97}	2026-02-05 22:53:03
1568	81	129	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 98}	2026-02-05 22:53:03
1569	81	157	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 99}	2026-02-05 22:53:03
1570	81	167	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 100}	2026-02-05 22:53:03
1571	107	157	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 101}	2026-02-05 22:53:03
1572	107	167	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 102}	2026-02-05 22:53:03
1573	129	157	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 103}	2026-02-05 22:53:03
1574	129	167	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 104}	2026-02-05 22:53:03
1575	157	167	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 105}	2026-02-05 22:53:03
1576	113	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 106}	2026-02-05 22:53:03
1577	1	118	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 107}	2026-02-05 22:53:03
1578	1	119	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 108}	2026-02-05 22:53:03
1579	107	118	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 109}	2026-02-05 22:53:03
1580	107	119	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 110}	2026-02-05 22:53:03
1581	113	153	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 111}	2026-02-05 22:53:03
1582	81	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 112}	2026-02-05 22:53:03
1583	107	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 113}	2026-02-05 22:53:03
1584	1	176	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 114}	2026-02-05 22:53:03
1585	2	176	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 115}	2026-02-05 22:53:03
1586	127	176	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 116}	2026-02-05 22:53:03
1587	1	177	associated_with	4	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 117}	2026-02-05 22:53:03
1588	152	177	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 118}	2026-02-05 22:53:03
1589	81	112	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 119}	2026-02-05 22:53:03
1590	1	179	associated_with	3	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 120}	2026-02-05 22:53:03
1591	139	152	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 121}	2026-02-05 22:53:03
1592	1	182	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 122}	2026-02-05 22:53:03
1593	1	184	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 123}	2026-02-05 22:53:03
1594	155	184	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 124}	2026-02-05 22:53:03
1595	147	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 125}	2026-02-05 22:53:03
1596	8	113	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 126}	2026-02-05 22:53:03
1597	8	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 127}	2026-02-05 22:53:03
1598	81	113	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 128}	2026-02-05 22:53:03
1599	107	113	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 129}	2026-02-05 22:53:03
1600	1	190	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 130}	2026-02-05 22:53:03
1601	1	192	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 131}	2026-02-05 22:53:03
1602	2	192	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 132}	2026-02-05 22:53:03
1603	1	194	associated_with	1	\N	\N	{"notes": "Co-appeared on 10 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 133}	2026-02-05 22:53:03
1604	81	152	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 134}	2026-02-05 22:53:03
1605	107	152	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 135}	2026-02-05 22:53:03
1606	152	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 136}	2026-02-05 22:53:03
1607	195	196	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 137}	2026-02-05 22:53:03
1608	155	194	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 138}	2026-02-05 22:53:03
1609	127	155	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 139}	2026-02-05 22:53:03
1610	1	200	associated_with	6	\N	\N	{"notes": "Co-appeared on 10 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 140}	2026-02-05 22:53:03
1611	2	200	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 141}	2026-02-05 22:53:03
1612	1	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 185 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 142}	2026-02-05 22:53:03
1613	2	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 153 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 143}	2026-02-05 22:53:03
1614	127	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 21 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 144}	2026-02-05 22:53:03
1615	155	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 145}	2026-02-05 22:53:03
1616	8	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 146}	2026-02-05 22:53:03
1617	81	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 147}	2026-02-05 22:53:03
1618	107	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 148}	2026-02-05 22:53:03
1619	1	204	associated_with	26	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 149}	2026-02-05 22:53:03
1620	2	204	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 150}	2026-02-05 22:53:03
1621	203	204	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 151}	2026-02-05 22:53:03
1622	1	208	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 152}	2026-02-05 22:53:03
1623	1	209	associated_with	1	\N	\N	{"notes": "Co-appeared on 10 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 153}	2026-02-05 22:53:03
1624	1	210	associated_with	2	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 154}	2026-02-05 22:53:03
1625	113	209	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 155}	2026-02-05 22:53:03
1626	118	210	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 156}	2026-02-05 22:53:03
1627	119	210	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 157}	2026-02-05 22:53:03
1628	113	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 10 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 158}	2026-02-05 22:53:03
1629	203	209	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 159}	2026-02-05 22:53:03
1630	1	211	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 160}	2026-02-05 22:53:03
1631	1	212	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 161}	2026-02-05 22:53:03
1632	2	118	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 162}	2026-02-05 22:53:03
1633	2	119	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 163}	2026-02-05 22:53:03
1634	2	211	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 164}	2026-02-05 22:53:03
1635	2	212	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 165}	2026-02-05 22:53:03
1636	118	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 166}	2026-02-05 22:53:03
1637	119	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 167}	2026-02-05 22:53:03
1638	211	212	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 168}	2026-02-05 22:53:03
1639	1	213	associated_with	7	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 169}	2026-02-05 22:53:03
1640	2	213	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 170}	2026-02-05 22:53:03
1641	203	213	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 171}	2026-02-05 22:53:03
1642	1	214	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 172}	2026-02-05 22:53:03
1643	2	214	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 173}	2026-02-05 22:53:03
1644	113	214	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 174}	2026-02-05 22:53:03
1645	203	214	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 175}	2026-02-05 22:53:03
1646	1	215	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 176}	2026-02-05 22:53:03
1647	112	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 177}	2026-02-05 22:53:03
1648	2	209	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 178}	2026-02-05 22:53:03
1649	7	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 179}	2026-02-05 22:53:03
1650	127	209	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 180}	2026-02-05 22:53:03
1651	160	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 181}	2026-02-05 22:53:03
1652	1	218	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 182}	2026-02-05 22:53:03
1653	2	218	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 183}	2026-02-05 22:53:03
1654	203	218	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 184}	2026-02-05 22:53:03
1655	1	222	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 185}	2026-02-05 22:53:03
1656	1	224	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 186}	2026-02-05 22:53:03
1657	1	225	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 187}	2026-02-05 22:53:03
1658	1	226	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 188}	2026-02-05 22:53:03
1659	1	227	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 189}	2026-02-05 22:53:03
1660	1	233	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 190}	2026-02-05 22:53:03
1661	1	234	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 191}	2026-02-05 22:53:03
1662	233	234	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 192}	2026-02-05 22:53:03
1663	1	236	associated_with	3	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 193}	2026-02-05 22:53:03
1664	2	236	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 194}	2026-02-05 22:53:03
1665	203	236	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 195}	2026-02-05 22:53:03
1666	1	237	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 196}	2026-02-05 22:53:03
1667	2	237	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 197}	2026-02-05 22:53:03
1668	1	239	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 198}	2026-02-05 22:53:03
1669	2	239	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 199}	2026-02-05 22:53:03
1670	127	239	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 200}	2026-02-05 22:53:03
1671	203	239	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 201}	2026-02-05 22:53:03
1672	2	240	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 202}	2026-02-05 22:53:03
1673	200	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 203}	2026-02-05 22:53:03
1674	200	240	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 204}	2026-02-05 22:53:03
1675	203	240	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 205}	2026-02-05 22:53:03
1676	1	240	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 206}	2026-02-05 22:53:03
1677	1	241	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 207}	2026-02-05 22:53:03
1678	2	241	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 208}	2026-02-05 22:53:03
1679	127	241	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 209}	2026-02-05 22:53:03
1680	203	241	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 210}	2026-02-05 22:53:03
1681	1	242	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 211}	2026-02-05 22:53:03
1682	1	245	associated_with	1	\N	\N	{"notes": "Co-appeared on 30 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 212}	2026-02-05 22:53:03
1683	2	222	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 213}	2026-02-05 22:53:03
1684	2	245	associated_with	1	\N	\N	{"notes": "Co-appeared on 12 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 214}	2026-02-05 22:53:03
1685	1	247	associated_with	1	\N	\N	{"notes": "Co-appeared on 13 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 215}	2026-02-05 22:53:03
1686	2	247	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 216}	2026-02-05 22:53:03
1687	203	247	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 217}	2026-02-05 22:53:03
1688	203	222	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 218}	2026-02-05 22:53:03
1689	1	250	associated_with	4	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 219}	2026-02-05 22:53:03
1690	200	236	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 220}	2026-02-05 22:53:03
1691	1	251	associated_with	26	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 221}	2026-02-05 22:53:03
1692	1	254	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 222}	2026-02-05 22:53:03
1693	1	256	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 223}	2026-02-05 22:53:03
1694	127	256	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 224}	2026-02-05 22:53:03
1695	203	256	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 225}	2026-02-05 22:53:03
1696	2	256	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 226}	2026-02-05 22:53:03
1697	257	258	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 227}	2026-02-05 22:53:03
1698	2	259	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 228}	2026-02-05 22:53:03
1699	200	256	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 229}	2026-02-05 22:53:03
1700	200	259	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 230}	2026-02-05 22:53:03
1701	236	256	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 231}	2026-02-05 22:53:03
1702	236	259	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 232}	2026-02-05 22:53:03
1703	256	259	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 233}	2026-02-05 22:53:03
1704	1	259	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 234}	2026-02-05 22:53:03
1705	1	260	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 235}	2026-02-05 22:53:03
1706	2	260	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 236}	2026-02-05 22:53:03
1707	1	258	associated_with	1	\N	\N	{"notes": "Co-appeared on 18 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 237}	2026-02-05 22:53:03
1708	1	265	associated_with	1	\N	\N	{"notes": "Co-appeared on 11 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 238}	2026-02-05 22:53:03
1709	1	257	associated_with	1	\N	\N	{"notes": "Co-appeared on 32 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 239}	2026-02-05 22:53:03
1710	112	257	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 240}	2026-02-05 22:53:03
1711	2	258	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 241}	2026-02-05 22:53:03
1712	127	258	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 242}	2026-02-05 22:53:03
1713	127	260	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 243}	2026-02-05 22:53:03
1714	258	260	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 244}	2026-02-05 22:53:03
1715	203	266	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 245}	2026-02-05 22:53:03
1716	203	258	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 246}	2026-02-05 22:53:03
1717	2	190	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 247}	2026-02-05 22:53:03
1718	190	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 248}	2026-02-05 22:53:03
1719	1	269	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 249}	2026-02-05 22:53:03
1720	203	269	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 250}	2026-02-05 22:53:03
1721	247	258	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 251}	2026-02-05 22:53:03
1722	1	270	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 252}	2026-02-05 22:53:03
1723	127	270	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 253}	2026-02-05 22:53:03
1724	203	270	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 254}	2026-02-05 22:53:03
1725	1	273	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 255}	2026-02-05 22:53:03
1726	2	273	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 256}	2026-02-05 22:53:03
1727	1	274	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 257}	2026-02-05 22:53:03
1728	2	274	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 258}	2026-02-05 22:53:03
1729	203	274	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 259}	2026-02-05 22:53:03
1730	203	245	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 260}	2026-02-05 22:53:03
1731	200	245	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 261}	2026-02-05 22:53:03
1732	1	277	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 262}	2026-02-05 22:53:03
1733	2	265	associated_with	1	\N	\N	{"notes": "Co-appeared on 10 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 263}	2026-02-05 22:53:03
1734	1	285	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 264}	2026-02-05 22:53:03
1735	1	297	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 265}	2026-02-05 22:53:03
1736	1	298	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 266}	2026-02-05 22:53:03
1737	2	298	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 267}	2026-02-05 22:53:03
1738	203	298	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 268}	2026-02-05 22:53:03
1739	2	250	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 269}	2026-02-05 22:53:03
1740	2	297	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 270}	2026-02-05 22:53:03
1741	203	297	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 271}	2026-02-05 22:53:03
1742	245	297	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 272}	2026-02-05 22:53:03
1743	1	301	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 273}	2026-02-05 22:53:03
1744	2	301	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 274}	2026-02-05 22:53:03
1745	203	301	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 275}	2026-02-05 22:53:03
1746	1	302	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 276}	2026-02-05 22:53:03
1747	257	302	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 277}	2026-02-05 22:53:03
1748	1	85	associated_with	8	\N	\N	{"notes": "Co-appeared on 22 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 278}	2026-02-05 22:53:03
1749	85	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 14 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 279}	2026-02-05 22:53:03
1750	1	305	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 280}	2026-02-05 22:53:03
1751	2	305	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 281}	2026-02-05 22:53:03
1752	10	265	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 282}	2026-02-05 22:53:03
1753	265	305	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 283}	2026-02-05 22:53:03
1754	1	306	associated_with	1	\N	\N	{"notes": "Co-appeared on 12 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 284}	2026-02-05 22:53:03
1755	2	306	associated_with	1	\N	\N	{"notes": "Co-appeared on 12 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 285}	2026-02-05 22:53:03
1756	85	245	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 286}	2026-02-05 22:53:03
1757	85	200	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 287}	2026-02-05 22:53:03
1758	85	236	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 288}	2026-02-05 22:53:03
1759	85	306	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 289}	2026-02-05 22:53:03
1760	203	306	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 290}	2026-02-05 22:53:03
1761	1	331	associated_with	1	\N	\N	{"notes": "Co-appeared on 24 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 291}	2026-02-05 22:53:03
1762	2	331	associated_with	1	\N	\N	{"notes": "Co-appeared on 20 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 292}	2026-02-05 22:53:03
1763	265	331	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 293}	2026-02-05 22:53:03
1764	265	306	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 294}	2026-02-05 22:53:03
1765	306	331	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 295}	2026-02-05 22:53:03
1766	1	333	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 296}	2026-02-05 22:53:03
1767	2	333	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 297}	2026-02-05 22:53:03
1768	305	306	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 298}	2026-02-05 22:53:03
1769	305	331	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 299}	2026-02-05 22:53:03
1770	85	331	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 300}	2026-02-05 22:53:03
1771	203	331	associated_with	1	\N	\N	{"notes": "Co-appeared on 12 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 301}	2026-02-05 22:53:03
1772	1	336	associated_with	11	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 302}	2026-02-05 22:53:03
1773	1	337	associated_with	3	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 303}	2026-02-05 22:53:03
1774	2	336	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 304}	2026-02-05 22:53:03
1775	2	337	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 305}	2026-02-05 22:53:03
1776	336	337	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 306}	2026-02-05 22:53:03
1777	194	339	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 307}	2026-02-05 22:53:03
1778	1	340	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 308}	2026-02-05 22:53:03
1779	203	340	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 309}	2026-02-05 22:53:03
1780	331	340	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 310}	2026-02-05 22:53:03
1781	160	218	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 311}	2026-02-05 22:53:03
1782	1	342	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 312}	2026-02-05 22:53:03
1783	2	342	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 313}	2026-02-05 22:53:03
1784	203	342	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 314}	2026-02-05 22:53:03
1785	203	260	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 315}	2026-02-05 22:53:03
1786	1	360	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 316}	2026-02-05 22:53:03
1787	2	360	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 317}	2026-02-05 22:53:03
1788	1	361	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 318}	2026-02-05 22:53:03
1789	2	361	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 319}	2026-02-05 22:53:03
1790	203	333	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 320}	2026-02-05 22:53:03
1791	203	360	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 321}	2026-02-05 22:53:03
1792	1	368	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 322}	2026-02-05 22:53:03
1793	2	368	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 323}	2026-02-05 22:53:03
1794	203	368	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 324}	2026-02-05 22:53:03
1795	247	368	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 325}	2026-02-05 22:53:03
1796	10	203	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 326}	2026-02-05 22:53:03
1797	1	375	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 327}	2026-02-05 22:53:03
1798	1	377	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 328}	2026-02-05 22:53:03
1799	10	360	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 329}	2026-02-05 22:53:03
1800	1	378	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 330}	2026-02-05 22:53:03
1801	10	378	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 331}	2026-02-05 22:53:03
1802	1	381	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 332}	2026-02-05 22:53:03
1803	10	218	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 333}	2026-02-05 22:53:03
1804	1	383	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 334}	2026-02-05 22:53:03
1805	10	361	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 335}	2026-02-05 22:53:03
1806	1	384	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 336}	2026-02-05 22:53:03
1807	2	384	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 337}	2026-02-05 22:53:03
1808	10	368	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 338}	2026-02-05 22:53:03
1809	10	384	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 339}	2026-02-05 22:53:03
1810	368	384	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 340}	2026-02-05 22:53:03
1811	1	387	associated_with	1	\N	\N	{"notes": "Co-appeared on 35 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 341}	2026-02-05 22:53:03
1812	1	388	associated_with	1	\N	\N	{"notes": "Co-appeared on 11 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 342}	2026-02-05 22:53:03
1813	387	388	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 343}	2026-02-05 22:53:03
1814	1	390	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 344}	2026-02-05 22:53:03
1815	9	10	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 345}	2026-02-05 22:53:03
1816	9	387	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 346}	2026-02-05 22:53:03
1817	10	387	associated_with	1	\N	\N	{"notes": "Co-appeared on 18 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 347}	2026-02-05 22:53:03
1818	10	388	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 348}	2026-02-05 22:53:03
1819	10	390	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 349}	2026-02-05 22:53:03
1820	387	390	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 350}	2026-02-05 22:53:03
1821	388	390	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 351}	2026-02-05 22:53:03
1822	1	391	associated_with	1	\N	\N	{"notes": "Co-appeared on 27 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 352}	2026-02-05 22:53:03
1823	388	391	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 353}	2026-02-05 22:53:03
1824	387	391	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 354}	2026-02-05 22:53:03
1825	10	391	associated_with	1	\N	\N	{"notes": "Co-appeared on 17 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 355}	2026-02-05 22:53:03
1826	2	387	associated_with	1	\N	\N	{"notes": "Co-appeared on 11 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 356}	2026-02-05 22:53:03
1827	2	391	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 357}	2026-02-05 22:53:03
1828	245	387	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 358}	2026-02-05 22:53:03
1829	2	388	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 359}	2026-02-05 22:53:03
1830	1	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 124 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 360}	2026-02-05 22:53:03
1831	1	399	associated_with	1	\N	\N	{"notes": "Co-appeared on 48 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 361}	2026-02-05 22:53:03
1832	10	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 77 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 362}	2026-02-05 22:53:03
1833	10	399	associated_with	1	\N	\N	{"notes": "Co-appeared on 29 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 363}	2026-02-05 22:53:03
1834	387	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 18 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 364}	2026-02-05 22:53:03
1835	387	399	associated_with	1	\N	\N	{"notes": "Co-appeared on 16 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 365}	2026-02-05 22:53:03
1836	388	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 366}	2026-02-05 22:53:03
1837	398	399	associated_with	1	\N	\N	{"notes": "Co-appeared on 38 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 367}	2026-02-05 22:53:03
1838	1	401	associated_with	24	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 368}	2026-02-05 22:53:03
1839	10	401	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 369}	2026-02-05 22:53:03
1840	391	399	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 370}	2026-02-05 22:53:03
1841	399	401	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 371}	2026-02-05 22:53:03
1842	2	399	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 372}	2026-02-05 22:53:03
1843	10	245	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 373}	2026-02-05 22:53:03
1844	1	406	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 374}	2026-02-05 22:53:03
1845	1	407	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 375}	2026-02-05 22:53:03
1846	10	13	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 376}	2026-02-05 22:53:03
1847	10	406	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 377}	2026-02-05 22:53:03
1848	10	407	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 378}	2026-02-05 22:53:03
1849	13	391	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 379}	2026-02-05 22:53:03
1850	13	406	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 380}	2026-02-05 22:53:03
1851	13	407	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 381}	2026-02-05 22:53:03
1852	391	406	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 382}	2026-02-05 22:53:03
1853	391	407	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 383}	2026-02-05 22:53:03
1854	406	407	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 384}	2026-02-05 22:53:03
1855	2	13	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 385}	2026-02-05 22:53:03
1856	2	406	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 386}	2026-02-05 22:53:03
1857	2	407	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 387}	2026-02-05 22:53:03
1858	1	408	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 388}	2026-02-05 22:53:03
1859	2	408	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 389}	2026-02-05 22:53:03
1860	10	408	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 390}	2026-02-05 22:53:03
1861	13	408	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 391}	2026-02-05 22:53:03
1862	391	408	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 392}	2026-02-05 22:53:03
1863	406	408	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 393}	2026-02-05 22:53:03
1864	8	387	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 394}	2026-02-05 22:53:03
1865	81	387	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 395}	2026-02-05 22:53:03
1866	107	387	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 396}	2026-02-05 22:53:03
1867	1	416	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 397}	2026-02-05 22:53:03
1868	10	416	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 398}	2026-02-05 22:53:03
1869	398	416	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 399}	2026-02-05 22:53:03
1870	1	418	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 400}	2026-02-05 22:53:03
1871	2	418	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 401}	2026-02-05 22:53:03
1872	1	422	associated_with	91	\N	\N	{"notes": "Co-appeared on 126 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 402}	2026-02-05 22:53:03
1873	2	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 20 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 403}	2026-02-05 22:53:03
1874	2	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 29 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 404}	2026-02-05 22:53:03
1875	9	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 11 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 405}	2026-02-05 22:53:03
1876	9	418	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 406}	2026-02-05 22:53:03
1877	9	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 14 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 407}	2026-02-05 22:53:03
1878	398	418	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 408}	2026-02-05 22:53:03
1879	398	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 94 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 409}	2026-02-05 22:53:03
1880	418	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 410}	2026-02-05 22:53:03
1881	1	423	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 411}	2026-02-05 22:53:03
1882	2	423	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 412}	2026-02-05 22:53:03
1883	81	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 413}	2026-02-05 22:53:03
1884	81	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 414}	2026-02-05 22:53:03
1885	81	423	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 415}	2026-02-05 22:53:03
1886	107	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 416}	2026-02-05 22:53:03
1887	107	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 417}	2026-02-05 22:53:03
1888	107	423	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 418}	2026-02-05 22:53:03
1889	398	423	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 419}	2026-02-05 22:53:03
1890	422	423	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 420}	2026-02-05 22:53:03
1891	10	418	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 421}	2026-02-05 22:53:03
1892	10	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 85 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 422}	2026-02-05 22:53:03
1893	1	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 77 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 423}	2026-02-05 22:53:03
1894	10	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 55 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 424}	2026-02-05 22:53:03
1895	398	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 65 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 425}	2026-02-05 22:53:03
1896	399	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 32 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 426}	2026-02-05 22:53:03
1897	399	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 23 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 427}	2026-02-05 22:53:03
1898	418	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 428}	2026-02-05 22:53:03
1899	422	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 75 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 429}	2026-02-05 22:53:03
1900	387	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 14 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 430}	2026-02-05 22:53:03
1901	387	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 431}	2026-02-05 22:53:03
1902	391	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 432}	2026-02-05 22:53:03
1903	391	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 433}	2026-02-05 22:53:03
1904	391	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 434}	2026-02-05 22:53:03
1905	1	425	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 435}	2026-02-05 22:53:03
1906	9	399	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 436}	2026-02-05 22:53:03
1907	9	425	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 437}	2026-02-05 22:53:03
1908	387	425	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 438}	2026-02-05 22:53:03
1909	398	425	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 439}	2026-02-05 22:53:03
1910	399	425	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 440}	2026-02-05 22:53:03
1911	422	425	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 441}	2026-02-05 22:53:03
1912	7	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 442}	2026-02-05 22:53:03
1913	245	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 443}	2026-02-05 22:53:03
1914	2	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 16 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 444}	2026-02-05 22:53:03
1915	2	425	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 445}	2026-02-05 22:53:03
1916	9	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 446}	2026-02-05 22:53:03
1917	424	425	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 447}	2026-02-05 22:53:03
1918	398	401	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 448}	2026-02-05 22:53:03
1919	401	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 449}	2026-02-05 22:53:03
1920	218	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 450}	2026-02-05 22:53:03
1921	218	399	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 451}	2026-02-05 22:53:03
1922	1	428	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 452}	2026-02-05 22:53:03
1923	10	428	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 453}	2026-02-05 22:53:03
1924	398	428	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 454}	2026-02-05 22:53:03
1925	10	251	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 455}	2026-02-05 22:53:03
1926	251	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 456}	2026-02-05 22:53:03
1927	1	429	associated_with	2	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 457}	2026-02-05 22:53:03
1928	10	429	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 458}	2026-02-05 22:53:03
1929	422	429	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 459}	2026-02-05 22:53:03
1930	424	429	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 460}	2026-02-05 22:53:03
1931	1	433	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 461}	2026-02-05 22:53:03
1932	245	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 462}	2026-02-05 22:53:03
1933	245	429	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 463}	2026-02-05 22:53:03
1934	245	433	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 464}	2026-02-05 22:53:03
1935	398	429	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 465}	2026-02-05 22:53:03
1936	398	433	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 466}	2026-02-05 22:53:03
1937	424	433	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 467}	2026-02-05 22:53:03
1938	429	433	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 468}	2026-02-05 22:53:03
1939	1	434	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 469}	2026-02-05 22:53:03
1940	1	435	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 470}	2026-02-05 22:53:03
1941	10	434	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 471}	2026-02-05 22:53:03
1942	10	435	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 472}	2026-02-05 22:53:03
1943	245	434	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 473}	2026-02-05 22:53:03
1944	245	435	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 474}	2026-02-05 22:53:03
1945	398	434	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 475}	2026-02-05 22:53:03
1946	398	435	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 476}	2026-02-05 22:53:03
1947	434	435	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 477}	2026-02-05 22:53:03
1948	387	439	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 478}	2026-02-05 22:53:03
1949	398	439	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 479}	2026-02-05 22:53:03
1950	10	433	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 480}	2026-02-05 22:53:03
1951	399	429	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 481}	2026-02-05 22:53:03
1952	399	433	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 482}	2026-02-05 22:53:03
1953	1	442	associated_with	5	\N	\N	{"notes": "Co-appeared on 23 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 483}	2026-02-05 22:53:03
1954	10	442	associated_with	1	\N	\N	{"notes": "Co-appeared on 18 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 484}	2026-02-05 22:53:03
1955	422	433	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 485}	2026-02-05 22:53:03
1956	422	442	associated_with	1	\N	\N	{"notes": "Co-appeared on 20 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 486}	2026-02-05 22:53:03
1957	424	442	associated_with	1	\N	\N	{"notes": "Co-appeared on 14 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 487}	2026-02-05 22:53:03
1958	398	442	associated_with	1	\N	\N	{"notes": "Co-appeared on 18 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 488}	2026-02-05 22:53:03
1959	429	442	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 489}	2026-02-05 22:53:03
1960	10	81	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 490}	2026-02-05 22:53:03
1961	10	107	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 491}	2026-02-05 22:53:03
1962	81	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 492}	2026-02-05 22:53:03
1963	107	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 493}	2026-02-05 22:53:03
1964	6	10	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 494}	2026-02-05 22:53:03
1965	6	398	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 495}	2026-02-05 22:53:03
1966	6	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 496}	2026-02-05 22:53:03
1967	6	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 497}	2026-02-05 22:53:03
1968	1	449	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 498}	2026-02-05 22:53:03
1969	10	449	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 499}	2026-02-05 22:53:03
1970	388	422	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 500}	2026-02-05 22:53:03
1971	388	424	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 501}	2026-02-05 22:53:03
1972	388	442	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 502}	2026-02-05 22:53:03
1973	2	442	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 503}	2026-02-05 22:53:03
1974	1	450	associated_with	1	\N	\N	{"notes": "Co-appeared on 12 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 504}	2026-02-05 22:53:03
1975	10	450	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 505}	2026-02-05 22:53:03
1976	398	450	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 506}	2026-02-05 22:53:03
1977	422	450	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 507}	2026-02-05 22:53:03
1978	424	450	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 508}	2026-02-05 22:53:03
1979	1	451	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 509}	2026-02-05 22:53:03
1980	9	442	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 510}	2026-02-05 22:53:03
1981	9	451	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 511}	2026-02-05 22:53:03
1982	10	451	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 512}	2026-02-05 22:53:03
1983	398	451	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 513}	2026-02-05 22:53:03
1984	422	451	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 514}	2026-02-05 22:53:03
1985	442	451	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 515}	2026-02-05 22:53:03
1986	1	452	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 516}	2026-02-05 22:53:03
1987	422	452	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 517}	2026-02-05 22:53:03
1988	10	452	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 518}	2026-02-05 22:53:03
1989	398	452	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 519}	2026-02-05 22:53:03
1990	424	452	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 520}	2026-02-05 22:53:03
1991	442	452	associated_with	1	\N	\N	{"notes": "Co-appeared on 5 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 521}	2026-02-05 22:53:03
1992	422	457	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 522}	2026-02-05 22:53:03
1993	424	457	associated_with	1	\N	\N	{"notes": "Co-appeared on 6 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 523}	2026-02-05 22:53:03
1994	442	450	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 524}	2026-02-05 22:53:03
1995	450	452	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 525}	2026-02-05 22:53:03
1996	2	458	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 526}	2026-02-05 22:53:03
1997	1	457	associated_with	1	\N	\N	{"notes": "Co-appeared on 21 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 527}	2026-02-05 22:53:03
1998	10	457	associated_with	1	\N	\N	{"notes": "Co-appeared on 9 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 528}	2026-02-05 22:53:03
1999	398	457	associated_with	1	\N	\N	{"notes": "Co-appeared on 13 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 529}	2026-02-05 22:53:03
2000	442	457	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 530}	2026-02-05 22:53:03
2001	452	457	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 531}	2026-02-05 22:53:03
2002	1	459	associated_with	1	\N	\N	{"notes": "Co-appeared on 11 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 532}	2026-02-05 22:53:03
2003	401	450	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 533}	2026-02-05 22:53:03
2004	422	459	associated_with	1	\N	\N	{"notes": "Co-appeared on 7 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 534}	2026-02-05 22:53:03
2005	450	457	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 535}	2026-02-05 22:53:03
2006	2	460	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 536}	2026-02-05 22:53:03
2007	2	461	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 537}	2026-02-05 22:53:03
2008	460	461	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 538}	2026-02-05 22:53:03
2009	10	459	associated_with	1	\N	\N	{"notes": "Co-appeared on 8 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 539}	2026-02-05 22:53:03
2010	457	459	associated_with	1	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 540}	2026-02-05 22:53:03
2011	1	462	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 541}	2026-02-05 22:53:03
2012	10	462	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 542}	2026-02-05 22:53:03
2013	459	462	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 543}	2026-02-05 22:53:03
2014	2	459	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 544}	2026-02-05 22:53:03
2015	1	469	associated_with	2	\N	\N	{"notes": "Co-appeared on 4 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 545}	2026-02-05 22:53:03
2016	10	469	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 546}	2026-02-05 22:53:03
2017	398	469	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 547}	2026-02-05 22:53:03
2018	424	469	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 548}	2026-02-05 22:53:03
2019	457	469	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 549}	2026-02-05 22:53:03
2020	1	470	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 550}	2026-02-05 22:53:03
2021	457	470	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 551}	2026-02-05 22:53:03
2022	469	470	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 552}	2026-02-05 22:53:03
2023	398	459	associated_with	1	\N	\N	{"notes": "Co-appeared on 2 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 553}	2026-02-05 22:53:03
2024	424	459	associated_with	1	\N	\N	{"notes": "Co-appeared on 3 flights together (from flight logs)", "original_type": "friend", "evidence_relationship_id": 554}	2026-02-05 22:53:03
2025	1	19	associated_with	286	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=21", "original_type": "other", "evidence_relationship_id": 555}	2026-02-05 22:53:03
2026	3	19	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=23", "original_type": "other", "evidence_relationship_id": 556}	2026-02-05 22:53:03
2027	6	13	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=223", "original_type": "other", "evidence_relationship_id": 557}	2026-02-05 22:53:03
2028	6	14	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=223", "original_type": "other", "evidence_relationship_id": 558}	2026-02-05 22:53:03
2029	13	14	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=223", "original_type": "other", "evidence_relationship_id": 559}	2026-02-05 22:53:03
2030	2	14	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=226", "original_type": "other", "evidence_relationship_id": 560}	2026-02-05 22:53:03
2031	13	85	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=230", "original_type": "other", "evidence_relationship_id": 561}	2026-02-05 22:53:03
2032	6	85	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=231", "original_type": "other", "evidence_relationship_id": 562}	2026-02-05 22:53:03
2033	7	14	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=232", "original_type": "other", "evidence_relationship_id": 563}	2026-02-05 22:53:03
2034	7	85	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=232", "original_type": "other", "evidence_relationship_id": 564}	2026-02-05 22:53:03
2035	14	85	associated_with	1	\N	\N	{"notes": "Co-mentioned in evidence document. Source: evidence_findings.jsonl id=232", "original_type": "other", "evidence_relationship_id": 565}	2026-02-05 22:53:03
2036	474	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2037	475	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2038	476	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2039	477	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2040	478	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2041	479	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2042	480	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2043	481	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2044	482	1	owned_by	1	\N	\N	{"note": "Epstein controlled entity", "source": "known_ownership"}	2026-02-05 22:53:03
2045	483	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2046	487	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2047	490	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2048	484	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2049	485	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2050	486	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2051	488	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2052	489	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2053	491	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2054	492	1	owned_by	1	\N	\N	{"note": "Epstein property", "source": "known_ownership"}	2026-02-05 22:53:03
2055	493	1	owned_by	1	\N	\N	{"note": "Epstein aircraft", "source": "known_ownership"}	2026-02-05 22:53:03
2056	494	1	owned_by	1	\N	\N	{"note": "Epstein aircraft", "source": "known_ownership"}	2026-02-05 22:53:03
2057	495	1	owned_by	1	\N	\N	{"note": "Epstein aircraft", "source": "known_ownership"}	2026-02-05 22:53:03
2059	82	1	associated_with	30	\N	\N	{"efta": "EFTA01660636", "detail": "Named in FBI PROMINENT NAMES briefing; victim allegation of massage directed by Maxwell; also trust beneficiary", "source": "ds10_fbi_prominent_names", "evidence_type": "single_testimony", "ds10_mention_count": 16}	2026-02-06 00:37:44
2060	7	1	associated_with	43	\N	\N	{"efta": "EFTA01660636", "detail": "Named in FBI PROMINENT NAMES briefing; victim allegation of massage on plane (victim noted as not a minor)", "source": "ds10_fbi_prominent_names", "evidence_type": "single_testimony", "ds10_mention_count": 36}	2026-02-06 00:37:45
2061	509	1	associated_with	13	\N	\N	{"detail": "Epstein sold Lutnick home for $10, later sold for millions; neighbors", "source": "ds10_fbi_prominent_names", "relationship_subtype": "financial_property"}	2026-02-06 00:37:45
2062	510	1	associated_with	234	\N	\N	{"efta": "EFTA01660636", "detail": "Named in FBI PROMINENT NAMES briefing; NTOC tip alleging present during abuses; victim encounter at model event", "source": "ds10_fbi_prominent_names", "evidence_type": "single_testimony", "ds10_mention_count": 229}	2026-02-06 00:37:45
2063	511	1	associated_with	14	\N	\N	{"efta": "EFTA02154241", "detail": "Breakfast meeting scheduled with Epstein per calendar (EFTA02154241)", "source": "ds10_analysis", "evidence_type": "documentary_only", "ds10_mention_count": 7}	2026-02-06 00:37:45
2064	512	1	communicated_with	6	\N	\N	{"efta": "EFTA02176329", "detail": "Scheduling email for lunch meeting; also reference to H.E. Sheikh", "source": "ds10_email"}	2026-02-06 00:37:46
2065	513	1	associated_with	4	\N	\N	{"efta": "EFTA01660636", "detail": "Named in unverified NTOC tip alongside Dershowitz; no contact info provided by tipster", "source": "ds10_analysis", "evidence_type": "circumstantial", "ds10_mention_count": 2}	2026-02-06 00:37:46
2066	514	1	associated_with	12	\N	\N	{"efta": "EFTA01660636", "detail": "Named in single unverified NTOC anonymous tip only; no corroboration; FBI could not follow up (no contact info)", "source": "ds10_analysis", "evidence_type": "circumstantial", "ds10_mention_count": 6}	2026-02-06 00:37:46
2067	515	1	associated_with	4	\N	\N	{"efta": "EFTA01660636", "detail": "Mentioned in NTOC tip context and FBI PROMINENT NAMES briefing", "source": "ds10_analysis", "evidence_type": "circumstantial", "ds10_mention_count": 2}	2026-02-06 00:37:46
2068	516	1	associated_with	4	\N	\N	{"efta": "EFTA01660636", "detail": "Source of allegations about Lutnick in FBI PROMINENT NAMES briefing", "source": "ds10_analysis", "evidence_type": "single_testimony", "ds10_mention_count": 2}	2026-02-06 00:37:46
2069	517	1	associated_with	4	\N	\N	{"efta": "EFTA01660636", "detail": "Witness named in FBI PROMINENT NAMES briefing re: Prince Andrew; noted as having criminal history", "source": "ds10_analysis", "evidence_type": "single_testimony", "ds10_mention_count": 2}	2026-02-06 00:37:46
2070	518	1	employed_by	10	\N	\N	{"efta": "EFTA01660623", "detail": "Former employee; source of black book; convicted of obstruction 2010", "source": "ds10_fbi_timeline"}	2026-02-06 00:37:46
2071	519	1	associated_with	2	\N	\N	{"detail": "MCC cellmate of Epstein", "source": "ds10_fbi_90a_case", "relationship_subtype": "mcc_cellmate"}	2026-02-06 00:37:46
2072	520	1	associated_with	3	\N	\N	{"detail": "MCC cellmate of Epstein", "source": "ds10_fbi_90a_case", "relationship_subtype": "mcc_cellmate"}	2026-02-06 00:37:46
2073	521	1	associated_with	6	\N	\N	{"efta": "EFTA01660625", "detail": "MCC CO on duty during Epstein death; charged and DPA", "source": "ds10_analysis", "evidence_type": "corroborated_documentary", "ds10_mention_count": 3}	2026-02-06 00:37:46
2074	522	1	associated_with	1	\N	\N	{"efta": "EFTA01660625", "detail": "MCC CO charged with conspiracy re: Epstein death; DPA", "source": "ds10_analysis", "evidence_type": "corroborated_documentary", "ds10_mention_count": 0}	2026-02-06 00:37:46
2075	2	503	associated_with	1	\N	\N	{"detail": "Multiple trust accounts and bank relationships found in DS10 hidden text", "source": "ds10_trust_beneficiary", "relationship_subtype": "beneficiary"}	2026-02-06 00:37:46
2076	2	497	associated_with	1	\N	\N	{"detail": "DS10 bank records for Ghislaine Maxwell", "source": "ds10_financial", "relationship_subtype": "banking_relationship"}	2026-02-06 00:37:46
2077	523	503	associated_with	1	\N	\N	{"detail": "Named as beneficiary in Insurance Trust and suite connections with Epstein", "source": "ds10_trust_beneficiary", "relationship_subtype": "beneficiary"}	2026-02-06 00:37:46
2078	523	502	associated_with	1	\N	\N	{"detail": "Named as beneficiary in Insurance Trust and suite connections with Epstein", "source": "ds10_trust_beneficiary", "relationship_subtype": "beneficiary"}	2026-02-06 00:37:46
2079	523	497	associated_with	1	\N	\N	{"detail": "DS10 bank records for Karyna Shuliak", "source": "ds10_financial", "relationship_subtype": "banking_relationship"}	2026-02-06 00:37:46
2080	39	504	associated_with	1	\N	\N	{"detail": "Trust relationship found in DS10; attorney/trustee role", "source": "ds10_trust_beneficiary", "relationship_subtype": "beneficiary"}	2026-02-06 00:37:46
2081	67	504	associated_with	1	\N	\N	{"detail": "Attorney/trustee appearing extensively in DS10 financial/trust documents", "source": "ds10_trust_beneficiary", "relationship_subtype": "beneficiary"}	2026-02-06 00:37:46
2082	67	503	associated_with	1	\N	\N	{"detail": "Attorney/trustee appearing extensively in DS10 financial/trust documents", "source": "ds10_trust_beneficiary", "relationship_subtype": "beneficiary"}	2026-02-06 00:37:46
2083	67	497	associated_with	1	\N	\N	{"detail": "DS10 bank records for Darren Indyke", "source": "ds10_financial", "relationship_subtype": "banking_relationship"}	2026-02-06 00:37:46
2084	1	497	associated_with	5	\N	\N	{"detail": "Epstein accounts at Deutsche Bank found in DS10 documents", "source": "ds10_financial"}	2026-02-06 00:37:46
2085	1	498	associated_with	5	\N	\N	{"detail": "Epstein accounts at JPMorgan Chase found in DS10 documents", "source": "ds10_financial"}	2026-02-06 00:37:46
2086	1	501	associated_with	5	\N	\N	{"detail": "Epstein accounts at SunTrust found in DS10 documents", "source": "ds10_financial"}	2026-02-06 00:37:46
2087	1	499	associated_with	5	\N	\N	{"detail": "Epstein accounts at Deutsche Bank Securities Inc. found in DS10 documents", "source": "ds10_financial"}	2026-02-06 00:37:46
2088	1	500	associated_with	5	\N	\N	{"detail": "Epstein accounts at Deutsche Bank Trust Co Americas found in DS10 documents", "source": "ds10_financial"}	2026-02-06 00:37:46
2089	1	506	associated_with	10	\N	\N	{"detail": "Multiple FBI investigations spanning 2006-2019", "source": "ds10_fbi_timeline", "fbi_cases": {"31E-MM-1080": "Initial Epstein investigation", "50D-NY-30275": "Epstein-related NY investigation", "72-MM-113327": "Obstruction case (Alfredo Rodriguez / black book)", "90A-NY-31512": "MCC death investigation (90A case)"}, "relationship_subtype": "investigation_subject"}	2026-02-06 00:37:46
2090	2	506	associated_with	8	\N	\N	{"detail": "Indicted 6/29/2020, arrested 7/2/2020, convicted 12/30/2021, sentenced to 20 years", "source": "ds10_fbi_timeline", "relationship_subtype": "investigation_subject"}	2026-02-06 00:37:46
2091	1	507	associated_with	5	\N	\N	{"detail": "Detained at MCC 7/8/2019; suicide 8/10/2019", "source": "ds10_fbi_timeline", "relationship_subtype": "detained_at"}	2026-02-06 00:37:46
2092	521	507	employed_by	1	\N	\N	{"detail": "Corrections officer charged re: Epstein death", "source": "ds10_fbi_90a_case"}	2026-02-06 00:37:46
2093	522	507	employed_by	1	\N	\N	{"detail": "Corrections officer charged re: Epstein death", "source": "ds10_fbi_90a_case"}	2026-02-06 00:37:46
2094	510	3	associated_with	2	\N	\N	{"detail": "Co-named in NTOC tip: both alleged present during abuses (EFTA01660636)", "source": "ds10_fbi_prominent_names"}	2026-02-06 00:37:46
2095	7	513	associated_with	1	\N	\N	{"detail": "Co-named in unverified NTOC tip as attorneys present at events", "source": "ds10_ntoc_tip"}	2026-02-06 00:37:46
2096	511	1	communicated_with	2	\N	\N	{"efta": "EFTA02154241", "detail": "Breakfast meeting scheduled: '8:30am Breakfast w/Ehud Barak' (Wed Nov 28)", "source": "ds10_calendar"}	2026-02-06 00:37:46
2575	710	59	communicated_with	680	2009-11-12	2017-03-25	{"a_to_b": 27, "b_to_a": 653, "source": "communications_db", "email_count": 680}	2026-02-18 02:51:29
2576	59	39	communicated_with	437	2011-11-10	2019-05-22	{"a_to_b": 350, "b_to_a": 87, "source": "communications_db", "email_count": 437}	2026-02-18 02:51:29
2577	59	12	communicated_with	208	2014-08-13	2019-04-22	{"a_to_b": 149, "b_to_a": 59, "source": "communications_db", "email_count": 208}	2026-02-18 02:51:29
2578	59	711	communicated_with	194	\N	\N	{"a_to_b": 190, "b_to_a": 4, "source": "communications_db", "email_count": 194}	2026-02-18 02:51:29
2579	712	59	communicated_with	184	\N	\N	{"a_to_b": 11, "b_to_a": 173, "source": "communications_db", "email_count": 184}	2026-02-18 02:51:29
2580	59	713	communicated_with	157	2014-05-09	2014-05-09	{"a_to_b": 96, "b_to_a": 61, "source": "communications_db", "email_count": 157}	2026-02-18 02:51:29
2581	714	39	communicated_with	156	2014-05-16	2019-02-14	{"a_to_b": 98, "b_to_a": 58, "source": "communications_db", "email_count": 156}	2026-02-18 02:51:29
2582	204	59	communicated_with	143	2010-03-11	2011-11-15	{"a_to_b": 35, "b_to_a": 108, "source": "communications_db", "email_count": 143}	2026-02-18 02:51:29
2583	715	59	communicated_with	142	2010-12-08	2010-12-08	{"a_to_b": 11, "b_to_a": 131, "source": "communications_db", "email_count": 142}	2026-02-18 02:51:29
2584	59	716	communicated_with	127	\N	\N	{"a_to_b": 97, "b_to_a": 30, "source": "communications_db", "email_count": 127}	2026-02-18 02:51:29
2585	59	717	communicated_with	126	\N	\N	{"a_to_b": 123, "b_to_a": 3, "source": "communications_db", "email_count": 126}	2026-02-18 02:51:29
2586	718	59	communicated_with	94	\N	\N	{"a_to_b": 17, "b_to_a": 77, "source": "communications_db", "email_count": 94}	2026-02-18 02:51:29
2587	719	59	communicated_with	93	\N	\N	{"a_to_b": 3, "b_to_a": 90, "source": "communications_db", "email_count": 93}	2026-02-18 02:51:29
2588	720	59	communicated_with	90	\N	\N	{"a_to_b": 0, "b_to_a": 90, "source": "communications_db", "email_count": 90}	2026-02-18 02:51:29
2589	59	721	communicated_with	89	\N	\N	{"a_to_b": 88, "b_to_a": 1, "source": "communications_db", "email_count": 89}	2026-02-18 02:51:29
2590	59	303	communicated_with	80	2013-01-04	2013-01-04	{"a_to_b": 70, "b_to_a": 10, "source": "communications_db", "email_count": 80}	2026-02-18 02:51:29
2591	722	59	communicated_with	76	2016-08-28	2016-08-28	{"a_to_b": 22, "b_to_a": 54, "source": "communications_db", "email_count": 76}	2026-02-18 02:51:29
2592	59	723	communicated_with	72	\N	\N	{"a_to_b": 72, "b_to_a": 0, "source": "communications_db", "email_count": 72}	2026-02-18 02:51:29
2593	67	59	communicated_with	68	2014-11-04	2018-12-05	{"a_to_b": 18, "b_to_a": 50, "source": "communications_db", "email_count": 68}	2026-02-18 02:51:29
2594	724	59	communicated_with	67	2011-05-09	2018-10-22	{"a_to_b": 10, "b_to_a": 57, "source": "communications_db", "email_count": 67}	2026-02-18 02:51:29
2595	12	39	communicated_with	64	2014-11-06	2017-05-04	{"a_to_b": 32, "b_to_a": 32, "source": "communications_db", "email_count": 64}	2026-02-18 02:51:29
2596	725	39	communicated_with	64	2016-06-02	2018-09-20	{"a_to_b": 36, "b_to_a": 28, "source": "communications_db", "email_count": 64}	2026-02-18 02:51:29
2597	726	59	communicated_with	64	2016-11-04	2018-12-07	{"a_to_b": 19, "b_to_a": 45, "source": "communications_db", "email_count": 64}	2026-02-18 02:51:29
2598	727	59	communicated_with	61	\N	\N	{"a_to_b": 2, "b_to_a": 59, "source": "communications_db", "email_count": 61}	2026-02-18 02:51:29
2599	59	728	communicated_with	59	\N	\N	{"a_to_b": 59, "b_to_a": 0, "source": "communications_db", "email_count": 59}	2026-02-18 02:51:29
2600	67	39	communicated_with	57	2014-03-24	2018-01-29	{"a_to_b": 20, "b_to_a": 37, "source": "communications_db", "email_count": 57}	2026-02-18 02:51:29
2601	59	729	communicated_with	52	2013-10-09	2015-01-12	{"a_to_b": 51, "b_to_a": 1, "source": "communications_db", "email_count": 52}	2026-02-18 02:51:29
2602	59	422	communicated_with	50	2015-03-20	2017-05-02	{"a_to_b": 35, "b_to_a": 15, "source": "communications_db", "email_count": 50}	2026-02-18 02:51:29
2603	59	730	communicated_with	49	0201-11-02	2014-28-04	{"a_to_b": 45, "b_to_a": 4, "source": "communications_db", "email_count": 49}	2026-02-18 02:51:29
2604	422	39	communicated_with	40	2015-10-23	2017-11-09	{"a_to_b": 15, "b_to_a": 25, "source": "communications_db", "email_count": 40}	2026-02-18 02:51:29
2605	59	731	communicated_with	38	2016-06-10	2016-06-10	{"a_to_b": 16, "b_to_a": 22, "source": "communications_db", "email_count": 38}	2026-02-18 02:51:29
2606	59	732	communicated_with	38	\N	\N	{"a_to_b": 9, "b_to_a": 29, "source": "communications_db", "email_count": 38}	2026-02-18 02:51:29
2607	59	523	communicated_with	37	2016-11-28	2018-04-13	{"a_to_b": 27, "b_to_a": 10, "source": "communications_db", "email_count": 37}	2026-02-18 02:51:29
2608	59	733	communicated_with	35	2014-09-12	2014-09-12	{"a_to_b": 35, "b_to_a": 0, "source": "communications_db", "email_count": 35}	2026-02-18 02:51:29
2609	59	734	communicated_with	34	2013-08-02	2013-08-02	{"a_to_b": 34, "b_to_a": 0, "source": "communications_db", "email_count": 34}	2026-02-18 02:51:29
2610	735	59	communicated_with	34	\N	\N	{"a_to_b": 1, "b_to_a": 33, "source": "communications_db", "email_count": 34}	2026-02-18 02:51:29
2611	729	39	communicated_with	34	2014-05-30	2014-10-20	{"a_to_b": 3, "b_to_a": 31, "source": "communications_db", "email_count": 34}	2026-02-18 02:51:29
2612	523	39	communicated_with	33	2014-05-30	2018-03-12	{"a_to_b": 18, "b_to_a": 15, "source": "communications_db", "email_count": 33}	2026-02-18 02:51:29
2613	736	59	communicated_with	33	2012-12-04	2018-06-22	{"a_to_b": 19, "b_to_a": 14, "source": "communications_db", "email_count": 33}	2026-02-18 02:51:29
2614	59	737	communicated_with	33	\N	\N	{"a_to_b": 31, "b_to_a": 2, "source": "communications_db", "email_count": 33}	2026-02-18 02:51:29
2615	59	738	communicated_with	32	2016-11-30	2016-11-30	{"a_to_b": 0, "b_to_a": 32, "source": "communications_db", "email_count": 32}	2026-02-18 02:51:29
2616	59	739	communicated_with	31	\N	\N	{"a_to_b": 31, "b_to_a": 0, "source": "communications_db", "email_count": 31}	2026-02-18 02:51:29
2617	714	67	communicated_with	31	2014-06-23	2016-03-21	{"a_to_b": 28, "b_to_a": 3, "source": "communications_db", "email_count": 31}	2026-02-18 02:51:29
2618	711	39	communicated_with	31	\N	\N	{"a_to_b": 26, "b_to_a": 5, "source": "communications_db", "email_count": 31}	2026-02-18 02:51:29
2619	12	729	communicated_with	30	2013-04-23	2014-06-04	{"a_to_b": 30, "b_to_a": 0, "source": "communications_db", "email_count": 30}	2026-02-18 02:51:29
2620	714	12	communicated_with	29	2016-02-05	2019-05-16	{"a_to_b": 6, "b_to_a": 23, "source": "communications_db", "email_count": 29}	2026-02-18 02:51:29
2621	714	59	communicated_with	29	2015-07-23	2015-07-23	{"a_to_b": 25, "b_to_a": 4, "source": "communications_db", "email_count": 29}	2026-02-18 02:51:29
2622	59	740	communicated_with	29	\N	\N	{"a_to_b": 25, "b_to_a": 4, "source": "communications_db", "email_count": 29}	2026-02-18 02:51:29
2623	59	741	communicated_with	28	2009-04-24	2009-04-24	{"a_to_b": 22, "b_to_a": 6, "source": "communications_db", "email_count": 28}	2026-02-18 02:51:29
2624	59	742	communicated_with	28	\N	\N	{"a_to_b": 28, "b_to_a": 0, "source": "communications_db", "email_count": 28}	2026-02-18 02:51:29
2625	715	204	communicated_with	27	2010-09-29	2011-09-12	{"a_to_b": 15, "b_to_a": 12, "source": "communications_db", "email_count": 27}	2026-02-18 02:51:29
2626	743	744	communicated_with	26	\N	\N	{"a_to_b": 1, "b_to_a": 25, "source": "communications_db", "email_count": 26}	2026-02-18 02:51:29
2627	745	59	communicated_with	26	\N	\N	{"a_to_b": 1, "b_to_a": 25, "source": "communications_db", "email_count": 26}	2026-02-18 02:51:29
2628	736	39	communicated_with	25	2014-09-19	2018-07-31	{"a_to_b": 20, "b_to_a": 5, "source": "communications_db", "email_count": 25}	2026-02-18 02:51:29
2629	725	523	communicated_with	24	\N	\N	{"a_to_b": 15, "b_to_a": 9, "source": "communications_db", "email_count": 24}	2026-02-18 02:51:29
2630	59	746	communicated_with	24	2012-11-14	2012-11-14	{"a_to_b": 22, "b_to_a": 2, "source": "communications_db", "email_count": 24}	2026-02-18 02:51:29
2631	747	59	communicated_with	24	\N	\N	{"a_to_b": 0, "b_to_a": 24, "source": "communications_db", "email_count": 24}	2026-02-18 02:51:29
2632	77	59	communicated_with	23	\N	\N	{"a_to_b": 9, "b_to_a": 14, "source": "communications_db", "email_count": 23}	2026-02-18 02:51:29
2633	59	748	communicated_with	23	\N	\N	{"a_to_b": 18, "b_to_a": 5, "source": "communications_db", "email_count": 23}	2026-02-18 02:51:29
2634	12	717	communicated_with	21	\N	\N	{"a_to_b": 20, "b_to_a": 1, "source": "communications_db", "email_count": 21}	2026-02-18 02:51:29
2635	714	725	communicated_with	21	\N	\N	{"a_to_b": 3, "b_to_a": 18, "source": "communications_db", "email_count": 21}	2026-02-18 02:51:29
2636	732	711	communicated_with	20	\N	\N	{"a_to_b": 20, "b_to_a": 0, "source": "communications_db", "email_count": 20}	2026-02-18 02:51:29
2637	59	3	communicated_with	19	\N	\N	{"a_to_b": 19, "b_to_a": 0, "source": "communications_db", "email_count": 19}	2026-02-18 02:51:29
2638	12	716	communicated_with	18	\N	\N	{"a_to_b": 14, "b_to_a": 4, "source": "communications_db", "email_count": 18}	2026-02-18 02:51:29
2639	714	523	communicated_with	18	2016-03-09	2017-06-23	{"a_to_b": 9, "b_to_a": 9, "source": "communications_db", "email_count": 18}	2026-02-18 02:51:29
2640	725	59	communicated_with	17	2016-01-04	2016-01-04	{"a_to_b": 6, "b_to_a": 11, "source": "communications_db", "email_count": 17}	2026-02-18 02:51:29
2641	749	59	communicated_with	17	\N	\N	{"a_to_b": 10, "b_to_a": 7, "source": "communications_db", "email_count": 17}	2026-02-18 02:51:29
2642	67	12	communicated_with	15	2015-04-23	2018-05-22	{"a_to_b": 7, "b_to_a": 8, "source": "communications_db", "email_count": 15}	2026-02-18 02:51:29
2643	724	39	communicated_with	15	2017-07-21	2019-03-04	{"a_to_b": 10, "b_to_a": 5, "source": "communications_db", "email_count": 15}	2026-02-18 02:51:29
2644	713	39	communicated_with	14	\N	\N	{"a_to_b": 6, "b_to_a": 8, "source": "communications_db", "email_count": 14}	2026-02-18 02:51:29
2645	59	750	communicated_with	14	\N	\N	{"a_to_b": 13, "b_to_a": 1, "source": "communications_db", "email_count": 14}	2026-02-18 02:51:29
2646	213	59	communicated_with	14	\N	\N	{"a_to_b": 4, "b_to_a": 10, "source": "communications_db", "email_count": 14}	2026-02-18 02:51:29
2647	523	12	communicated_with	13	2016-03-15	2018-10-03	{"a_to_b": 6, "b_to_a": 7, "source": "communications_db", "email_count": 13}	2026-02-18 02:51:29
2648	422	12	communicated_with	13	\N	\N	{"a_to_b": 5, "b_to_a": 8, "source": "communications_db", "email_count": 13}	2026-02-18 02:51:29
2649	59	751	communicated_with	13	\N	\N	{"a_to_b": 13, "b_to_a": 0, "source": "communications_db", "email_count": 13}	2026-02-18 02:51:29
2650	752	59	communicated_with	13	\N	\N	{"a_to_b": 0, "b_to_a": 13, "source": "communications_db", "email_count": 13}	2026-02-18 02:51:29
2651	743	59	communicated_with	13	\N	\N	{"a_to_b": 1, "b_to_a": 12, "source": "communications_db", "email_count": 13}	2026-02-18 02:51:29
2652	724	12	communicated_with	12	\N	\N	{"a_to_b": 5, "b_to_a": 7, "source": "communications_db", "email_count": 12}	2026-02-18 02:51:29
2653	107	59	communicated_with	12	2016-05-01	2018-06-27	{"a_to_b": 7, "b_to_a": 5, "source": "communications_db", "email_count": 12}	2026-02-18 02:51:29
2654	59	753	communicated_with	12	2014-11-29	2014-11-29	{"a_to_b": 7, "b_to_a": 5, "source": "communications_db", "email_count": 12}	2026-02-18 02:51:29
2655	740	39	communicated_with	12	2012-07-18	2012-07-18	{"a_to_b": 0, "b_to_a": 12, "source": "communications_db", "email_count": 12}	2026-02-18 02:51:29
2656	754	39	communicated_with	12	2017-12-11	2019-03-12	{"a_to_b": 10, "b_to_a": 2, "source": "communications_db", "email_count": 12}	2026-02-18 02:51:29
2657	738	728	communicated_with	11	\N	\N	{"a_to_b": 11, "b_to_a": 0, "source": "communications_db", "email_count": 11}	2026-02-18 02:51:29
2658	59	755	communicated_with	11	2015-07-10	2015-07-10	{"a_to_b": 4, "b_to_a": 7, "source": "communications_db", "email_count": 11}	2026-02-18 02:51:29
2659	756	59	communicated_with	11	\N	\N	{"a_to_b": 3, "b_to_a": 8, "source": "communications_db", "email_count": 11}	2026-02-18 02:51:29
2660	59	757	communicated_with	11	\N	\N	{"a_to_b": 11, "b_to_a": 0, "source": "communications_db", "email_count": 11}	2026-02-18 02:51:29
2661	758	59	communicated_with	11	\N	\N	{"a_to_b": 4, "b_to_a": 7, "source": "communications_db", "email_count": 11}	2026-02-18 02:51:29
2662	718	12	communicated_with	10	\N	\N	{"a_to_b": 0, "b_to_a": 10, "source": "communications_db", "email_count": 10}	2026-02-18 02:51:29
2663	725	12	communicated_with	10	2015-02-02	2016-06-08	{"a_to_b": 6, "b_to_a": 4, "source": "communications_db", "email_count": 10}	2026-02-18 02:51:29
2664	712	12	communicated_with	10	\N	\N	{"a_to_b": 1, "b_to_a": 9, "source": "communications_db", "email_count": 10}	2026-02-18 02:51:29
2665	12	401	communicated_with	10	\N	\N	{"a_to_b": 10, "b_to_a": 0, "source": "communications_db", "email_count": 10}	2026-02-18 02:51:29
2666	59	759	communicated_with	10	\N	\N	{"a_to_b": 10, "b_to_a": 0, "source": "communications_db", "email_count": 10}	2026-02-18 02:51:29
2667	715	39	communicated_with	10	2011-02-24	2011-02-24	{"a_to_b": 10, "b_to_a": 0, "source": "communications_db", "email_count": 10}	2026-02-18 02:51:29
2668	59	4	communicated_with	9	2010-08-24	2010-08-24	{"a_to_b": 6, "b_to_a": 3, "source": "communications_db", "email_count": 9}	2026-02-18 02:51:29
2669	726	12	communicated_with	9	\N	\N	{"a_to_b": 1, "b_to_a": 8, "source": "communications_db", "email_count": 9}	2026-02-18 02:51:29
2670	710	760	communicated_with	9	2012-09-21	2012-09-21	{"a_to_b": 0, "b_to_a": 9, "source": "communications_db", "email_count": 9}	2026-02-18 02:51:29
2671	736	523	communicated_with	9	\N	\N	{"a_to_b": 4, "b_to_a": 5, "source": "communications_db", "email_count": 9}	2026-02-18 02:51:29
2672	511	59	communicated_with	9	\N	\N	{"a_to_b": 0, "b_to_a": 9, "source": "communications_db", "email_count": 9}	2026-02-18 02:51:29
2673	59	251	communicated_with	9	2014-03-08	2014-03-08	{"a_to_b": 9, "b_to_a": 0, "source": "communications_db", "email_count": 9}	2026-02-18 02:51:29
2674	714	754	communicated_with	8	2018-05-17	2019-04-30	{"a_to_b": 5, "b_to_a": 3, "source": "communications_db", "email_count": 8}	2026-02-18 02:51:29
2675	736	715	communicated_with	8	\N	\N	{"a_to_b": 5, "b_to_a": 3, "source": "communications_db", "email_count": 8}	2026-02-18 02:51:29
2676	7	59	communicated_with	8	2015-01-08	2015-01-08	{"a_to_b": 5, "b_to_a": 3, "source": "communications_db", "email_count": 8}	2026-02-18 02:51:29
2677	761	59	communicated_with	8	\N	\N	{"a_to_b": 2, "b_to_a": 6, "source": "communications_db", "email_count": 8}	2026-02-18 02:51:29
2678	762	59	communicated_with	8	\N	\N	{"a_to_b": 2, "b_to_a": 6, "source": "communications_db", "email_count": 8}	2026-02-18 02:51:29
2679	59	763	communicated_with	8	\N	\N	{"a_to_b": 4, "b_to_a": 4, "source": "communications_db", "email_count": 8}	2026-02-18 02:51:29
2680	714	729	communicated_with	8	2014-05-13	2014-09-29	{"a_to_b": 8, "b_to_a": 0, "source": "communications_db", "email_count": 8}	2026-02-18 02:51:29
2681	12	730	communicated_with	8	\N	\N	{"a_to_b": 8, "b_to_a": 0, "source": "communications_db", "email_count": 8}	2026-02-18 02:51:29
2682	761	12	communicated_with	7	2016-02-02	2016-02-02	{"a_to_b": 1, "b_to_a": 6, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2683	722	726	communicated_with	7	\N	\N	{"a_to_b": 2, "b_to_a": 5, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2684	712	764	communicated_with	7	\N	\N	{"a_to_b": 7, "b_to_a": 0, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2685	748	39	communicated_with	7	2018-09-09	2018-09-09	{"a_to_b": 2, "b_to_a": 5, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2686	732	39	communicated_with	7	2015-02-11	2015-04-12	{"a_to_b": 7, "b_to_a": 0, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2688	765	59	communicated_with	7	2014-19-11	2015-13-01	{"a_to_b": 0, "b_to_a": 7, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2689	77	710	communicated_with	7	\N	\N	{"a_to_b": 3, "b_to_a": 4, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2690	743	12	communicated_with	7	2011-08-02	2011-08-02	{"a_to_b": 0, "b_to_a": 7, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2691	766	39	communicated_with	7	2013-11-12	2014-01-14	{"a_to_b": 1, "b_to_a": 6, "source": "communications_db", "email_count": 7}	2026-02-18 02:51:29
2692	67	726	communicated_with	6	\N	\N	{"a_to_b": 3, "b_to_a": 3, "source": "communications_db", "email_count": 6}	2026-02-18 02:51:29
2693	726	39	communicated_with	6	2014-09-11	2016-11-04	{"a_to_b": 4, "b_to_a": 2, "source": "communications_db", "email_count": 6}	2026-02-18 02:51:29
2694	59	767	communicated_with	6	\N	\N	{"a_to_b": 2, "b_to_a": 4, "source": "communications_db", "email_count": 6}	2026-02-18 02:51:29
2695	12	768	communicated_with	6	2016-09-14	2019-05-10	{"a_to_b": 5, "b_to_a": 1, "source": "communications_db", "email_count": 6}	2026-02-18 02:51:29
2696	725	715	communicated_with	6	2011-02-24	2011-02-24	{"a_to_b": 0, "b_to_a": 6, "source": "communications_db", "email_count": 6}	2026-02-18 02:51:29
2697	769	59	communicated_with	6	\N	\N	{"a_to_b": 0, "b_to_a": 6, "source": "communications_db", "email_count": 6}	2026-02-18 02:51:29
2698	722	725	communicated_with	6	\N	\N	{"a_to_b": 6, "b_to_a": 0, "source": "communications_db", "email_count": 6}	2026-02-18 02:51:29
2699	738	12	communicated_with	5	\N	\N	{"a_to_b": 5, "b_to_a": 0, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2700	12	770	communicated_with	5	\N	\N	{"a_to_b": 5, "b_to_a": 0, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2701	67	422	communicated_with	5	\N	\N	{"a_to_b": 0, "b_to_a": 5, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2702	720	12	communicated_with	5	\N	\N	{"a_to_b": 0, "b_to_a": 5, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2703	714	401	communicated_with	5	2016-06-29	2016-06-29	{"a_to_b": 2, "b_to_a": 3, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2704	736	725	communicated_with	5	\N	\N	{"a_to_b": 2, "b_to_a": 3, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2705	771	59	communicated_with	5	\N	\N	{"a_to_b": 1, "b_to_a": 4, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2706	213	204	communicated_with	5	\N	\N	{"a_to_b": 0, "b_to_a": 5, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2707	764	39	communicated_with	5	2015-04-16	2017-03-24	{"a_to_b": 4, "b_to_a": 1, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2708	204	39	communicated_with	5	\N	\N	{"a_to_b": 3, "b_to_a": 2, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2709	722	732	communicated_with	5	\N	\N	{"a_to_b": 3, "b_to_a": 2, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2710	710	39	communicated_with	5	\N	\N	{"a_to_b": 5, "b_to_a": 0, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2711	772	59	communicated_with	5	\N	\N	{"a_to_b": 5, "b_to_a": 0, "source": "communications_db", "email_count": 5}	2026-02-18 02:51:29
2712	12	748	communicated_with	4	\N	\N	{"a_to_b": 4, "b_to_a": 0, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2713	12	711	communicated_with	4	\N	\N	{"a_to_b": 4, "b_to_a": 0, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2714	727	67	communicated_with	4	\N	\N	{"a_to_b": 0, "b_to_a": 4, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2715	736	204	communicated_with	4	\N	\N	{"a_to_b": 4, "b_to_a": 0, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2716	8	59	communicated_with	4	\N	\N	{"a_to_b": 0, "b_to_a": 4, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2717	213	39	communicated_with	4	\N	\N	{"a_to_b": 4, "b_to_a": 0, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2718	738	768	communicated_with	4	\N	\N	{"a_to_b": 4, "b_to_a": 0, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2719	714	764	communicated_with	4	2015-04-16	2017-03-24	{"a_to_b": 1, "b_to_a": 3, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2720	59	773	communicated_with	4	\N	\N	{"a_to_b": 3, "b_to_a": 1, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2721	745	39	communicated_with	4	\N	\N	{"a_to_b": 0, "b_to_a": 4, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2722	774	59	communicated_with	4	\N	\N	{"a_to_b": 0, "b_to_a": 4, "source": "communications_db", "email_count": 4}	2026-02-18 02:51:29
2723	59	768	communicated_with	3	\N	\N	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2724	756	12	communicated_with	3	\N	\N	{"a_to_b": 2, "b_to_a": 1, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2725	107	12	communicated_with	3	2019-04-08	2019-04-08	{"a_to_b": 1, "b_to_a": 2, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2726	59	775	communicated_with	3	2013-11-12	2013-11-12	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2727	710	12	communicated_with	3	\N	\N	{"a_to_b": 0, "b_to_a": 3, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2728	59	776	communicated_with	3	\N	\N	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2729	715	12	communicated_with	3	\N	\N	{"a_to_b": 0, "b_to_a": 3, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2730	777	12	communicated_with	3	\N	\N	{"a_to_b": 0, "b_to_a": 3, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2731	177	59	communicated_with	3	2013-10-29	2013-12-04	{"a_to_b": 0, "b_to_a": 3, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2732	778	59	communicated_with	3	\N	\N	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2733	177	12	communicated_with	3	\N	\N	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2734	718	756	communicated_with	3	\N	\N	{"a_to_b": 0, "b_to_a": 3, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2735	719	722	communicated_with	3	\N	\N	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2736	710	730	communicated_with	3	2014-27-06	2014-27-06	{"a_to_b": 1, "b_to_a": 2, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2737	7	766	communicated_with	3	\N	\N	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2738	59	779	communicated_with	3	\N	\N	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2739	67	729	communicated_with	3	2015-10-01	2015-10-01	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2740	59	336	communicated_with	3	\N	\N	{"a_to_b": 0, "b_to_a": 3, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2741	772	39	communicated_with	3	\N	\N	{"a_to_b": 3, "b_to_a": 0, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2742	714	736	communicated_with	3	\N	\N	{"a_to_b": 2, "b_to_a": 1, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2743	762	712	communicated_with	3	\N	\N	{"a_to_b": 2, "b_to_a": 1, "source": "communications_db", "email_count": 3}	2026-02-18 02:51:29
2744	780	781	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2745	732	12	communicated_with	2	2015-10-01	2015-10-01	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2746	722	67	communicated_with	2	2015-02-03	2015-02-03	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2747	12	713	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2748	12	782	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2749	764	12	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2750	67	741	communicated_with	2	2009-04-24	2009-04-24	{"a_to_b": 1, "b_to_a": 1, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2751	735	422	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2752	781	59	communicated_with	2	2011-08-08	2011-08-08	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2753	783	12	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2754	251	12	communicated_with	2	2018-02-09	2018-11-25	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2755	754	59	communicated_with	2	2018-07-18	2018-07-18	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2756	7	741	communicated_with	2	2009-04-24	2009-04-24	{"a_to_b": 1, "b_to_a": 1, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2757	784	39	communicated_with	2	2014-12-24	2014-12-24	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2758	59	785	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2759	781	746	communicated_with	2	\N	\N	{"a_to_b": 1, "b_to_a": 1, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2760	712	39	communicated_with	2	2017-10-18	2017-10-18	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2761	781	39	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2762	59	786	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2763	336	39	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2764	59	787	communicated_with	2	\N	\N	{"a_to_b": 1, "b_to_a": 1, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2765	4	788	communicated_with	2	\N	\N	{"a_to_b": 1, "b_to_a": 1, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2766	729	713	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2767	59	788	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2768	710	765	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2769	789	59	communicated_with	2	\N	\N	{"a_to_b": 1, "b_to_a": 1, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2770	59	790	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2771	710	303	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2772	724	758	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2773	766	59	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2774	12	723	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2775	710	511	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2776	718	758	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2777	722	39	communicated_with	2	2015-10-06	2015-10-06	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2778	422	753	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2779	12	791	communicated_with	2	\N	\N	{"a_to_b": 0, "b_to_a": 2, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
2780	710	789	communicated_with	2	\N	\N	{"a_to_b": 2, "b_to_a": 0, "source": "communications_db", "email_count": 2}	2026-02-18 02:51:29
\.


--
-- Data for Name: edge_sources; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.edge_sources (id, relationship_id, source_type, source_id, source_detail, created_at) FROM stdin;
1	1486	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:44
2	1478	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:44
3	2059	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:44
4	1475	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:44
5	1473	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:44
6	1472	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:44
7	1474	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:45
8	2060	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:45
9	1485	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:45
10	2061	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:45
11	2062	ds10_redaction_analysis	\N	FBI PROMINENT NAMES (EFTA01660636)	2026-02-06 00:37:45
12	2063	ds10_redaction_analysis	\N	DS10 document (EFTA02154241)	2026-02-06 00:37:45
13	2064	ds10_redaction_analysis	\N	DS10 document (EFTA02176329)	2026-02-06 00:37:46
14	2065	ds10_redaction_analysis	\N	DS10 document (EFTA01660636)	2026-02-06 00:37:46
15	2066	ds10_redaction_analysis	\N	DS10 document (EFTA01660636)	2026-02-06 00:37:46
16	2067	ds10_redaction_analysis	\N	DS10 document (EFTA01660636)	2026-02-06 00:37:46
17	2068	ds10_redaction_analysis	\N	DS10 document (EFTA01660636)	2026-02-06 00:37:46
18	2069	ds10_redaction_analysis	\N	DS10 document (EFTA01660636)	2026-02-06 00:37:46
19	2070	ds10_redaction_analysis	\N	DS10 document (EFTA01660623)	2026-02-06 00:37:46
20	2071	ds10_redaction_analysis	\N	DS10 document (EFTA01660622)	2026-02-06 00:37:46
21	2072	ds10_redaction_analysis	\N	DS10 document (EFTA01660625)	2026-02-06 00:37:46
22	2073	ds10_redaction_analysis	\N	DS10 document (EFTA01660625)	2026-02-06 00:37:46
23	2074	ds10_redaction_analysis	\N	DS10 document (EFTA01660625)	2026-02-06 00:37:46
24	2075	ds10_financial_docs	\N	Trust beneficiary (multiple DS10 financial documents)	2026-02-06 00:37:46
25	2076	ds10_financial_docs	\N	Banking relationship	2026-02-06 00:37:46
26	2077	ds10_financial_docs	\N	Trust beneficiary (multiple DS10 financial documents)	2026-02-06 00:37:46
27	2078	ds10_financial_docs	\N	Trust beneficiary (multiple DS10 financial documents)	2026-02-06 00:37:46
28	2079	ds10_financial_docs	\N	Banking relationship	2026-02-06 00:37:46
29	2080	ds10_financial_docs	\N	Trust beneficiary (multiple DS10 financial documents)	2026-02-06 00:37:46
30	2081	ds10_financial_docs	\N	Trust beneficiary (multiple DS10 financial documents)	2026-02-06 00:37:46
31	2082	ds10_financial_docs	\N	Trust beneficiary (multiple DS10 financial documents)	2026-02-06 00:37:46
32	2083	ds10_financial_docs	\N	Banking relationship	2026-02-06 00:37:46
33	2084	ds10_financial_docs	\N	DS10 financial records	2026-02-06 00:37:46
34	2085	ds10_financial_docs	\N	DS10 financial records	2026-02-06 00:37:46
35	2086	ds10_financial_docs	\N	DS10 financial records	2026-02-06 00:37:46
36	2087	ds10_financial_docs	\N	DS10 financial records	2026-02-06 00:37:46
37	2088	ds10_financial_docs	\N	DS10 financial records	2026-02-06 00:37:46
38	2089	ds10_fbi_briefing	\N	EFTA01660622 FBI case timeline	2026-02-06 00:37:46
39	2090	ds10_fbi_briefing	\N	EFTA01660634 Maxwell trial summary	2026-02-06 00:37:46
1405	2575	email	\N	EFTA00421840	2026-02-18 02:51:29
1406	2575	email	\N	EFTA00648334	2026-02-18 02:51:29
1407	2575	email	\N	EFTA00638950	2026-02-18 02:51:29
1408	2575	email	\N	EFTA00648339	2026-02-18 02:51:29
1409	2575	email	\N	EFTA00406711	2026-02-18 02:51:29
1410	2576	email	\N	EFTA00370047	2026-02-18 02:51:29
1411	2576	email	\N	EFTA00313080	2026-02-18 02:51:29
1412	2576	email	\N	EFTA00370035	2026-02-18 02:51:29
1413	2576	email	\N	EFTA00370044	2026-02-18 02:51:29
1414	2576	email	\N	EFTA00366977	2026-02-18 02:51:29
1415	2577	email	\N	EFTA00336431	2026-02-18 02:51:29
1416	2577	email	\N	EFTA00364677	2026-02-18 02:51:29
1417	2577	email	\N	EFTA00333380	2026-02-18 02:51:29
1418	2577	email	\N	EFTA00358716	2026-02-18 02:51:29
1419	2577	email	\N	EFTA00333377	2026-02-18 02:51:29
1420	2578	email	\N	EFTA00329206	2026-02-18 02:51:29
1421	2578	email	\N	EFTA00626491	2026-02-18 02:51:29
1422	2578	email	\N	EFTA00644413	2026-02-18 02:51:29
1423	2578	email	\N	EFTA00645754	2026-02-18 02:51:29
1424	2578	email	\N	EFTA00329213	2026-02-18 02:51:29
1425	2579	email	\N	EFTA00691562	2026-02-18 02:51:29
1426	2579	email	\N	EFTA00658325	2026-02-18 02:51:29
1427	2579	email	\N	EFTA00690888	2026-02-18 02:51:29
1428	2579	email	\N	EFTA00697111	2026-02-18 02:51:29
1429	2579	email	\N	EFTA00813274	2026-02-18 02:51:29
1430	2580	email	\N	EFTA00631050	2026-02-18 02:51:29
1431	2580	email	\N	EFTA00364691	2026-02-18 02:51:29
1432	2580	email	\N	EFTA00634778	2026-02-18 02:51:29
1433	2580	email	\N	EFTA00683934	2026-02-18 02:51:29
1434	2580	email	\N	EFTA00693241	2026-02-18 02:51:29
1435	2581	email	\N	EFTA00359783	2026-02-18 02:51:29
1436	2581	email	\N	EFTA00547581	2026-02-18 02:51:29
1437	2581	email	\N	EFTA00547780	2026-02-18 02:51:29
1438	2581	email	\N	EFTA00533519	2026-02-18 02:51:29
1439	2581	email	\N	EFTA00540362	2026-02-18 02:51:29
1440	2582	email	\N	EFTA00733714	2026-02-18 02:51:29
1441	2582	email	\N	EFTA00736661	2026-02-18 02:51:29
1442	2582	email	\N	EFTA00709276	2026-02-18 02:51:29
1443	2582	email	\N	EFTA00682176	2026-02-18 02:51:29
1444	2582	email	\N	EFTA00705434	2026-02-18 02:51:29
1445	2583	email	\N	EFTA00642615	2026-02-18 02:51:29
1446	2583	email	\N	EFTA00709276	2026-02-18 02:51:29
1447	2583	email	\N	EFTA00733416	2026-02-18 02:51:29
1448	2583	email	\N	EFTA00648893	2026-02-18 02:51:29
1449	2583	email	\N	EFTA00731932	2026-02-18 02:51:29
1450	2584	email	\N	EFTA00700955	2026-02-18 02:51:29
1451	2584	email	\N	EFTA00673450	2026-02-18 02:51:29
1452	2584	email	\N	EFTA00712229	2026-02-18 02:51:29
1453	2584	email	\N	EFTA00393677	2026-02-18 02:51:29
1454	2584	email	\N	EFTA00647154	2026-02-18 02:51:29
1455	2585	email	\N	EFTA00643671	2026-02-18 02:51:29
1456	2585	email	\N	EFTA00851428	2026-02-18 02:51:29
1457	2585	email	\N	EFTA00842987	2026-02-18 02:51:29
1458	2585	email	\N	EFTA00851442	2026-02-18 02:51:29
1459	2585	email	\N	EFTA00851433	2026-02-18 02:51:29
1460	2586	email	\N	EFTA00836663	2026-02-18 02:51:29
1461	2586	email	\N	EFTA00836671	2026-02-18 02:51:29
1462	2586	email	\N	EFTA00680228	2026-02-18 02:51:29
1463	2586	email	\N	EFTA00715210	2026-02-18 02:51:29
1464	2586	email	\N	EFTA00714108	2026-02-18 02:51:29
1465	2587	email	\N	EFTA00710795	2026-02-18 02:51:29
1466	2587	email	\N	EFTA00752907	2026-02-18 02:51:29
1467	2587	email	\N	EFTA00750539	2026-02-18 02:51:29
1468	2587	email	\N	EFTA00752719	2026-02-18 02:51:29
1469	2587	email	\N	EFTA00749108	2026-02-18 02:51:29
1470	2588	email	\N	EFTA02391100	2026-02-18 02:51:29
1471	2588	email	\N	EFTA02347549	2026-02-18 02:51:29
1472	2588	email	\N	EFTA02377471	2026-02-18 02:51:29
1473	2588	email	\N	EFTA02215334	2026-02-18 02:51:29
1474	2588	email	\N	EFTA02372647	2026-02-18 02:51:29
1475	2589	email	\N	EFTA00766945	2026-02-18 02:51:29
1476	2589	email	\N	EFTA00756864	2026-02-18 02:51:29
1477	2589	email	\N	EFTA00894142	2026-02-18 02:51:29
1478	2589	email	\N	EFTA00712288	2026-02-18 02:51:29
1479	2589	email	\N	EFTA00756858	2026-02-18 02:51:29
1480	2590	email	\N	EFTA00373487	2026-02-18 02:51:29
1481	2590	email	\N	EFTA00540666	2026-02-18 02:51:29
1482	2590	email	\N	EFTA00472432	2026-02-18 02:51:29
1483	2590	email	\N	EFTA00540736	2026-02-18 02:51:29
1484	2590	email	\N	EFTA00838558	2026-02-18 02:51:29
1485	2591	email	\N	EFTA00406335	2026-02-18 02:51:29
1486	2591	email	\N	EFTA00406351	2026-02-18 02:51:29
1487	2591	email	\N	EFTA00428911	2026-02-18 02:51:29
1488	2591	email	\N	EFTA00659607	2026-02-18 02:51:29
1489	2591	email	\N	EFTA00351567	2026-02-18 02:51:29
1490	2592	email	\N	EFTA00920762	2026-02-18 02:51:29
1491	2592	email	\N	EFTA00740708	2026-02-18 02:51:29
1492	2592	email	\N	EFTA00868609	2026-02-18 02:51:29
1493	2592	email	\N	EFTA00753954	2026-02-18 02:51:29
1494	2592	email	\N	EFTA00923615	2026-02-18 02:51:29
1495	2593	email	\N	EFTA00732477	2026-02-18 02:51:29
1496	2593	email	\N	EFTA00351836	2026-02-18 02:51:29
1497	2593	email	\N	EFTA00393236	2026-02-18 02:51:29
1498	2593	email	\N	EFTA00390037	2026-02-18 02:51:29
1499	2593	email	\N	EFTA00422935	2026-02-18 02:51:29
1500	2594	email	\N	EFTA00675040	2026-02-18 02:51:29
1501	2594	email	\N	EFTA00898225	2026-02-18 02:51:29
1502	2594	email	\N	EFTA00777899	2026-02-18 02:51:29
1503	2594	email	\N	EFTA00753295	2026-02-18 02:51:29
1504	2594	email	\N	EFTA00753298	2026-02-18 02:51:29
1505	2595	email	\N	EFTA00446423	2026-02-18 02:51:29
1506	2595	email	\N	EFTA00321759	2026-02-18 02:51:29
1507	2595	email	\N	EFTA00336301	2026-02-18 02:51:29
1508	2595	email	\N	EFTA00337206	2026-02-18 02:51:29
1509	2595	email	\N	EFTA00362581	2026-02-18 02:51:29
1510	2596	email	\N	EFTA00540626	2026-02-18 02:51:29
1511	2596	email	\N	EFTA00540592	2026-02-18 02:51:29
1512	2596	email	\N	EFTA00826329	2026-02-18 02:51:29
1513	2596	email	\N	EFTA00547908	2026-02-18 02:51:29
1514	2596	email	\N	EFTA00546553	2026-02-18 02:51:29
1515	2597	email	\N	EFTA01737944	2026-02-18 02:51:29
1516	2597	email	\N	EFTA01029038	2026-02-18 02:51:29
1517	2597	email	\N	EFTA00378528	2026-02-18 02:51:29
1518	2597	email	\N	EFTA00378537	2026-02-18 02:51:29
1519	2597	email	\N	EFTA00820870	2026-02-18 02:51:29
1520	2598	email	\N	EFTA00672166	2026-02-18 02:51:29
1521	2598	email	\N	EFTA00932235	2026-02-18 02:51:29
1522	2598	email	\N	EFTA00702337	2026-02-18 02:51:29
1523	2598	email	\N	EFTA00932005	2026-02-18 02:51:29
1524	2598	email	\N	EFTA00662620	2026-02-18 02:51:29
1525	2599	email	\N	EFTA00357380	2026-02-18 02:51:29
1526	2599	email	\N	EFTA00357388	2026-02-18 02:51:29
1527	2599	email	\N	EFTA00528609	2026-02-18 02:51:29
1528	2599	email	\N	EFTA00981861	2026-02-18 02:51:29
1529	2599	email	\N	EFTA00357773	2026-02-18 02:51:29
1530	2600	email	\N	EFTA01047433	2026-02-18 02:51:29
1531	2600	email	\N	EFTA01401792	2026-02-18 02:51:29
1532	2600	email	\N	EFTA00799164	2026-02-18 02:51:29
1533	2600	email	\N	EFTA00901772	2026-02-18 02:51:29
1534	2600	email	\N	EFTA01352611	2026-02-18 02:51:29
1535	2601	email	\N	EFTA01193579	2026-02-18 02:51:29
1536	2601	email	\N	EFTA01404139	2026-02-18 02:51:29
1537	2601	email	\N	EFTA01193576	2026-02-18 02:51:29
1538	2601	email	\N	EFTA00715644	2026-02-18 02:51:29
1539	2601	email	\N	EFTA01401348	2026-02-18 02:51:29
1540	2602	email	\N	EFTA00330495	2026-02-18 02:51:29
1541	2602	email	\N	EFTA00331680	2026-02-18 02:51:29
1542	2602	email	\N	EFTA00972056	2026-02-18 02:51:29
1543	2602	email	\N	EFTA00330498	2026-02-18 02:51:29
1544	2602	email	\N	EFTA01957921	2026-02-18 02:51:29
1545	2603	email	\N	EFTA01764889	2026-02-18 02:51:29
1546	2603	email	\N	EFTA01751680	2026-02-18 02:51:29
1547	2603	email	\N	EFTA00721086	2026-02-18 02:51:29
1548	2603	email	\N	EFTA00992670	2026-02-18 02:51:29
1549	2603	email	\N	EFTA00663174	2026-02-18 02:51:29
1550	2604	email	\N	EFTA00368121	2026-02-18 02:51:29
1551	2604	email	\N	EFTA00321759	2026-02-18 02:51:29
1552	2604	email	\N	EFTA00374778	2026-02-18 02:51:29
1553	2604	email	\N	EFTA00932571	2026-02-18 02:51:29
1554	2604	email	\N	EFTA00409641	2026-02-18 02:51:29
1555	2605	email	\N	EFTA01839692	2026-02-18 02:51:29
1556	2605	email	\N	EFTA00931476	2026-02-18 02:51:29
1557	2605	email	\N	EFTA00931459	2026-02-18 02:51:29
1558	2605	email	\N	EFTA00718984	2026-02-18 02:51:29
1559	2605	email	\N	EFTA01840374	2026-02-18 02:51:29
1560	2606	email	\N	EFTA00758048	2026-02-18 02:51:29
1561	2606	email	\N	EFTA00681134	2026-02-18 02:51:29
1562	2606	email	\N	EFTA01020499	2026-02-18 02:51:29
1563	2606	email	\N	EFTA01022516	2026-02-18 02:51:29
1564	2606	email	\N	EFTA01800759	2026-02-18 02:51:29
1565	2607	email	\N	EFTA00566602	2026-02-18 02:51:29
1566	2607	email	\N	EFTA00539522	2026-02-18 02:51:29
1567	2607	email	\N	EFTA00529386	2026-02-18 02:51:29
1568	2607	email	\N	EFTA00536613	2026-02-18 02:51:29
1569	2607	email	\N	EFTA01914472	2026-02-18 02:51:29
1570	2608	email	\N	EFTA00368254	2026-02-18 02:51:29
1571	2608	email	\N	EFTA02467463	2026-02-18 02:51:29
1572	2608	email	\N	EFTA02356637	2026-02-18 02:51:29
1573	2608	email	\N	EFTA02060458	2026-02-18 02:51:29
1574	2608	email	\N	EFTA00835369	2026-02-18 02:51:29
1575	2609	email	\N	EFTA01842439	2026-02-18 02:51:29
1576	2609	email	\N	EFTA01738366	2026-02-18 02:51:29
1577	2609	email	\N	EFTA00721133	2026-02-18 02:51:29
1578	2609	email	\N	EFTA00751440	2026-02-18 02:51:29
1579	2609	email	\N	EFTA00419322	2026-02-18 02:51:29
1580	2610	email	\N	EFTA00991493	2026-02-18 02:51:29
1581	2610	email	\N	EFTA00964533	2026-02-18 02:51:29
1582	2610	email	\N	EFTA00970152	2026-02-18 02:51:29
1583	2610	email	\N	EFTA00964536	2026-02-18 02:51:29
1584	2610	email	\N	EFTA01790825	2026-02-18 02:51:29
1585	2611	email	\N	EFTA00862678	2026-02-18 02:51:29
1586	2611	email	\N	EFTA01412968	2026-02-18 02:51:29
1587	2611	email	\N	EFTA00862651	2026-02-18 02:51:29
1588	2611	email	\N	EFTA01421823	2026-02-18 02:51:29
1589	2611	email	\N	EFTA01468922	2026-02-18 02:51:29
1590	2612	email	\N	EFTA00534758	2026-02-18 02:51:29
1591	2612	email	\N	EFTA00574491	2026-02-18 02:51:29
1592	2612	email	\N	EFTA00564939	2026-02-18 02:51:29
1593	2612	email	\N	EFTA00570572	2026-02-18 02:51:29
1594	2612	email	\N	EFTA00567265	2026-02-18 02:51:29
1595	2613	email	\N	EFTA00733714	2026-02-18 02:51:29
1596	2613	email	\N	EFTA00751968	2026-02-18 02:51:29
1597	2613	email	\N	EFTA01788640	2026-02-18 02:51:29
1598	2613	email	\N	EFTA02002249	2026-02-18 02:51:29
1599	2613	email	\N	EFTA02007970	2026-02-18 02:51:29
1600	2614	email	\N	EFTA00882391	2026-02-18 02:51:29
1601	2614	email	\N	EFTA00671109	2026-02-18 02:51:29
1602	2614	email	\N	EFTA00776602	2026-02-18 02:51:29
1603	2614	email	\N	EFTA00879084	2026-02-18 02:51:29
1604	2614	email	\N	EFTA00749612	2026-02-18 02:51:29
1605	2615	email	\N	EFTA00327686	2026-02-18 02:51:29
1606	2615	email	\N	EFTA00377501	2026-02-18 02:51:29
1607	2615	email	\N	EFTA00448197	2026-02-18 02:51:29
1608	2615	email	\N	EFTA00439637	2026-02-18 02:51:29
1609	2615	email	\N	EFTA00448189	2026-02-18 02:51:29
1610	2616	email	\N	EFTA00419247	2026-02-18 02:51:29
1611	2616	email	\N	EFTA00467755	2026-02-18 02:51:29
1612	2616	email	\N	EFTA00854114	2026-02-18 02:51:29
1613	2616	email	\N	EFTA00870270	2026-02-18 02:51:29
1614	2616	email	\N	EFTA00397513	2026-02-18 02:51:29
1615	2617	email	\N	EFTA01404610	2026-02-18 02:51:29
1616	2617	email	\N	EFTA01401455	2026-02-18 02:51:29
1617	2617	email	\N	EFTA01413940	2026-02-18 02:51:29
1618	2617	email	\N	EFTA01412104	2026-02-18 02:51:29
1619	2617	email	\N	EFTA01405911	2026-02-18 02:51:29
1620	2618	email	\N	EFTA00925405	2026-02-18 02:51:29
1621	2618	email	\N	EFTA00911815	2026-02-18 02:51:29
1622	2618	email	\N	EFTA01003817	2026-02-18 02:51:29
1623	2618	email	\N	EFTA00940437	2026-02-18 02:51:29
1624	2618	email	\N	EFTA01005346	2026-02-18 02:51:29
1625	2619	email	\N	EFTA01351316	2026-02-18 02:51:29
1626	2619	email	\N	EFTA01351494	2026-02-18 02:51:29
1627	2619	email	\N	EFTA00328665	2026-02-18 02:51:29
1628	2619	email	\N	EFTA01351543	2026-02-18 02:51:29
1629	2619	email	\N	EFTA00460508	2026-02-18 02:51:29
1630	2620	email	\N	EFTA02045032	2026-02-18 02:51:29
1631	2620	email	\N	EFTA02059914	2026-02-18 02:51:29
1632	2620	email	\N	EFTA02196616	2026-02-18 02:51:29
1633	2620	email	\N	EFTA02098235	2026-02-18 02:51:29
1634	2620	email	\N	EFTA02098257	2026-02-18 02:51:29
1635	2621	email	\N	EFTA00890969	2026-02-18 02:51:29
1636	2621	email	\N	EFTA01436304	2026-02-18 02:51:29
1637	2621	email	\N	EFTA00851070	2026-02-18 02:51:29
1638	2621	email	\N	EFTA01420572	2026-02-18 02:51:29
1639	2621	email	\N	EFTA01022583	2026-02-18 02:51:29
1640	2622	email	\N	EFTA00697243	2026-02-18 02:51:29
1641	2622	email	\N	EFTA01861798	2026-02-18 02:51:29
1642	2622	email	\N	EFTA00755030	2026-02-18 02:51:29
1643	2622	email	\N	EFTA01047634	2026-02-18 02:51:29
1644	2622	email	\N	EFTA00897502	2026-02-18 02:51:29
1645	2623	email	\N	EFTA00743005	2026-02-18 02:51:29
1646	2623	email	\N	EFTA00732477	2026-02-18 02:51:29
1647	2623	email	\N	EFTA00905860	2026-02-18 02:51:29
1648	2623	email	\N	EFTA00697839	2026-02-18 02:51:29
1649	2623	email	\N	EFTA00649315	2026-02-18 02:51:29
1650	2624	email	\N	EFTA02518894	2026-02-18 02:51:29
1651	2624	email	\N	EFTA00881543	2026-02-18 02:51:29
1652	2624	email	\N	EFTA02523277	2026-02-18 02:51:29
1653	2624	email	\N	EFTA00881250	2026-02-18 02:51:29
1654	2624	email	\N	EFTA02523051	2026-02-18 02:51:29
1655	2625	email	\N	EFTA01795489	2026-02-18 02:51:29
1656	2625	email	\N	EFTA00900147	2026-02-18 02:51:29
1657	2625	email	\N	EFTA00900630	2026-02-18 02:51:29
1658	2625	email	\N	EFTA00905154	2026-02-18 02:51:29
1659	2625	email	\N	EFTA00900707	2026-02-18 02:51:29
1660	2626	email	\N	EFTA00210971	2026-02-18 02:51:29
1661	2626	email	\N	EFTA00206871	2026-02-18 02:51:29
1662	2626	email	\N	EFTA00205035	2026-02-18 02:51:29
1663	2626	email	\N	EFTA00210525	2026-02-18 02:51:29
1664	2626	email	\N	EFTA00205269	2026-02-18 02:51:29
1665	2627	email	\N	EFTA00847429	2026-02-18 02:51:29
1666	2627	email	\N	EFTA01744801	2026-02-18 02:51:29
1667	2627	email	\N	EFTA01193310	2026-02-18 02:51:29
1668	2627	email	\N	EFTA01847346	2026-02-18 02:51:29
1669	2627	email	\N	EFTA00639998	2026-02-18 02:51:29
1670	2628	email	\N	EFTA01048190	2026-02-18 02:51:29
1671	2628	email	\N	EFTA01016179	2026-02-18 02:51:29
1672	2628	email	\N	EFTA01877497	2026-02-18 02:51:29
1673	2628	email	\N	EFTA01902720	2026-02-18 02:51:29
1674	2628	email	\N	EFTA02061055	2026-02-18 02:51:29
1675	2629	email	\N	EFTA00546020	2026-02-18 02:51:29
1676	2629	email	\N	EFTA00548650	2026-02-18 02:51:29
1677	2629	email	\N	EFTA00571214	2026-02-18 02:51:29
1678	2629	email	\N	EFTA00546553	2026-02-18 02:51:29
1679	2629	email	\N	EFTA00552552	2026-02-18 02:51:29
1680	2630	email	\N	EFTA01762851	2026-02-18 02:51:29
1681	2630	email	\N	EFTA00962148	2026-02-18 02:51:29
1682	2630	email	\N	EFTA00951708	2026-02-18 02:51:29
1683	2630	email	\N	EFTA00951712	2026-02-18 02:51:29
1684	2630	email	\N	EFTA00951698	2026-02-18 02:51:29
1685	2631	email	\N	EFTA00665479	2026-02-18 02:51:29
1686	2631	email	\N	EFTA02608800	2026-02-18 02:51:29
1687	2631	email	\N	EFTA02608843	2026-02-18 02:51:29
1688	2631	email	\N	EFTA02371541	2026-02-18 02:51:29
1689	2631	email	\N	EFTA02396170	2026-02-18 02:51:29
1690	2632	email	\N	EFTA01142883	2026-02-18 02:51:29
1691	2632	email	\N	EFTA00986219	2026-02-18 02:51:29
1692	2632	email	\N	EFTA00977539	2026-02-18 02:51:29
1693	2632	email	\N	EFTA00966909	2026-02-18 02:51:29
1694	2632	email	\N	EFTA01964544	2026-02-18 02:51:29
1695	2633	email	\N	EFTA02638534	2026-02-18 02:51:29
1696	2633	email	\N	EFTA02543698	2026-02-18 02:51:29
1697	2633	email	\N	EFTA02647764	2026-02-18 02:51:29
1698	2633	email	\N	EFTA01042937	2026-02-18 02:51:29
1699	2633	email	\N	EFTA01044364	2026-02-18 02:51:29
1700	2634	email	\N	EFTA00459844	2026-02-18 02:51:29
1701	2634	email	\N	EFTA00460664	2026-02-18 02:51:29
1702	2634	email	\N	EFTA00330627	2026-02-18 02:51:29
1703	2634	email	\N	EFTA00460661	2026-02-18 02:51:29
1704	2634	email	\N	EFTA00321892	2026-02-18 02:51:29
1705	2635	email	\N	EFTA00547003	2026-02-18 02:51:29
1706	2635	email	\N	EFTA00547959	2026-02-18 02:51:29
1707	2635	email	\N	EFTA00547908	2026-02-18 02:51:29
1708	2635	email	\N	EFTA00548650	2026-02-18 02:51:29
1709	2635	email	\N	EFTA00548388	2026-02-18 02:51:29
1710	2636	email	\N	EFTA02476406	2026-02-18 02:51:29
1711	2636	email	\N	EFTA02486016	2026-02-18 02:51:29
1712	2636	email	\N	EFTA00416073	2026-02-18 02:51:29
1713	2636	email	\N	EFTA00660418	2026-02-18 02:51:29
1714	2636	email	\N	EFTA01800759	2026-02-18 02:51:29
1715	2637	email	\N	EFTA02400622	2026-02-18 02:51:29
1716	2637	email	\N	EFTA02651318	2026-02-18 02:51:29
1717	2637	email	\N	EFTA01054188	2026-02-18 02:51:29
1718	2637	email	\N	EFTA01047854	2026-02-18 02:51:29
1719	2637	email	\N	EFTA02448211	2026-02-18 02:51:29
1720	2638	email	\N	EFTA02395975	2026-02-18 02:51:29
1721	2638	email	\N	EFTA00385320	2026-02-18 02:51:29
1722	2638	email	\N	EFTA01969210	2026-02-18 02:51:29
1723	2638	email	\N	EFTA02242309	2026-02-18 02:51:29
1724	2638	email	\N	EFTA00379738	2026-02-18 02:51:29
1725	2639	email	\N	EFTA00540362	2026-02-18 02:51:29
1726	2639	email	\N	EFTA00546020	2026-02-18 02:51:29
1727	2639	email	\N	EFTA02301157	2026-02-18 02:51:29
1728	2639	email	\N	EFTA00575066	2026-02-18 02:51:29
1729	2639	email	\N	EFTA02323988	2026-02-18 02:51:29
1730	2640	email	\N	EFTA00639725	2026-02-18 02:51:29
1731	2640	email	\N	EFTA01873781	2026-02-18 02:51:29
1732	2640	email	\N	EFTA02694880	2026-02-18 02:51:29
1733	2640	email	\N	EFTA01880849	2026-02-18 02:51:29
1734	2640	email	\N	EFTA00677709	2026-02-18 02:51:29
1735	2641	email	\N	EFTA02509047	2026-02-18 02:51:29
1736	2641	email	\N	EFTA00717912	2026-02-18 02:51:29
1737	2641	email	\N	EFTA00855850	2026-02-18 02:51:29
1738	2641	email	\N	EFTA00845271	2026-02-18 02:51:29
1739	2641	email	\N	EFTA00832951	2026-02-18 02:51:29
1740	2642	email	\N	EFTA00437018	2026-02-18 02:51:29
1741	2642	email	\N	EFTA00376224	2026-02-18 02:51:29
1742	2642	email	\N	EFTA00351836	2026-02-18 02:51:29
1743	2642	email	\N	EFTA00442953	2026-02-18 02:51:29
1744	2642	email	\N	EFTA00376197	2026-02-18 02:51:29
1745	2643	email	\N	EFTA00570492	2026-02-18 02:51:29
1746	2643	email	\N	EFTA00472980	2026-02-18 02:51:29
1747	2643	email	\N	EFTA00570502	2026-02-18 02:51:29
1748	2643	email	\N	EFTA01018745	2026-02-18 02:51:29
1749	2643	email	\N	EFTA02377090	2026-02-18 02:51:29
1750	2644	email	\N	EFTA02082000	2026-02-18 02:51:29
1751	2644	email	\N	EFTA00643261	2026-02-18 02:51:29
1752	2644	email	\N	EFTA00861294	2026-02-18 02:51:29
1753	2644	email	\N	EFTA01194373	2026-02-18 02:51:29
1754	2644	email	\N	EFTA02507993	2026-02-18 02:51:29
1755	2645	email	\N	EFTA00777658	2026-02-18 02:51:29
1756	2645	email	\N	EFTA00752378	2026-02-18 02:51:29
1757	2645	email	\N	EFTA00752371	2026-02-18 02:51:29
1758	2645	email	\N	EFTA01981850	2026-02-18 02:51:29
1759	2645	email	\N	EFTA00679322	2026-02-18 02:51:29
1760	2646	email	\N	EFTA02527834	2026-02-18 02:51:29
1761	2646	email	\N	EFTA00733714	2026-02-18 02:51:29
1762	2646	email	\N	EFTA00736661	2026-02-18 02:51:29
1763	2646	email	\N	EFTA02434432	2026-02-18 02:51:29
1764	2646	email	\N	EFTA02414027	2026-02-18 02:51:29
1765	2647	email	\N	EFTA02043374	2026-02-18 02:51:29
1766	2647	email	\N	EFTA02142428	2026-02-18 02:51:29
1767	2647	email	\N	EFTA00449225	2026-02-18 02:51:29
1768	2647	email	\N	EFTA02043467	2026-02-18 02:51:29
1769	2647	email	\N	EFTA02059849	2026-02-18 02:51:29
1770	2648	email	\N	EFTA00387218	2026-02-18 02:51:29
1771	2648	email	\N	EFTA00369226	2026-02-18 02:51:29
1772	2648	email	\N	EFTA00391405	2026-02-18 02:51:29
1773	2648	email	\N	EFTA02065367	2026-02-18 02:51:29
1774	2648	email	\N	EFTA02089646	2026-02-18 02:51:29
1775	2649	email	\N	EFTA00995295	2026-02-18 02:51:29
1776	2649	email	\N	EFTA02533210	2026-02-18 02:51:29
1777	2649	email	\N	EFTA01057392	2026-02-18 02:51:29
1778	2649	email	\N	EFTA02665617	2026-02-18 02:51:29
1779	2649	email	\N	EFTA01057384	2026-02-18 02:51:29
1780	2650	email	\N	EFTA00900136	2026-02-18 02:51:29
1781	2650	email	\N	EFTA01826592	2026-02-18 02:51:29
1782	2650	email	\N	EFTA00891187	2026-02-18 02:51:29
1783	2650	email	\N	EFTA00764773	2026-02-18 02:51:29
1784	2650	email	\N	EFTA01831406	2026-02-18 02:51:29
1785	2651	email	\N	EFTA02714716	2026-02-18 02:51:29
1786	2651	email	\N	EFTA02484843	2026-02-18 02:51:29
1787	2651	email	\N	EFTA02354145	2026-02-18 02:51:29
1788	2651	email	\N	EFTA02484737	2026-02-18 02:51:29
1789	2651	email	\N	EFTA01028706	2026-02-18 02:51:29
1790	2652	email	\N	EFTA01855200	2026-02-18 02:51:29
1791	2652	email	\N	EFTA00428124	2026-02-18 02:51:29
1792	2652	email	\N	EFTA00382495	2026-02-18 02:51:29
1793	2652	email	\N	EFTA02251080	2026-02-18 02:51:29
1794	2652	email	\N	EFTA01855120	2026-02-18 02:51:29
1795	2653	email	\N	EFTA00740178	2026-02-18 02:51:29
1796	2653	email	\N	EFTA02356320	2026-02-18 02:51:29
1797	2653	email	\N	EFTA01793355	2026-02-18 02:51:29
1798	2653	email	\N	EFTA02178078	2026-02-18 02:51:29
1799	2653	email	\N	EFTA00770921	2026-02-18 02:51:29
1800	2654	email	\N	EFTA02089189	2026-02-18 02:51:29
1801	2654	email	\N	EFTA01980329	2026-02-18 02:51:29
1802	2654	email	\N	EFTA02434255	2026-02-18 02:51:29
1803	2654	email	\N	EFTA00767779	2026-02-18 02:51:29
1804	2654	email	\N	EFTA02300610	2026-02-18 02:51:29
1805	2655	email	\N	EFTA01888603	2026-02-18 02:51:29
1806	2655	email	\N	EFTA00941629	2026-02-18 02:51:29
1807	2655	email	\N	EFTA01876996	2026-02-18 02:51:29
1808	2655	email	\N	EFTA00940154	2026-02-18 02:51:29
1809	2655	email	\N	EFTA02360191	2026-02-18 02:51:29
1810	2656	email	\N	EFTA01033359	2026-02-18 02:51:29
1811	2656	email	\N	EFTA02622722	2026-02-18 02:51:29
1812	2656	email	\N	EFTA02666025	2026-02-18 02:51:29
1813	2656	email	\N	EFTA01021717	2026-02-18 02:51:29
1814	2656	email	\N	EFTA00947769	2026-02-18 02:51:29
1815	2657	email	\N	EFTA02118673	2026-02-18 02:51:29
1816	2657	email	\N	EFTA00362236	2026-02-18 02:51:29
1817	2657	email	\N	EFTA00377505	2026-02-18 02:51:29
1818	2657	email	\N	EFTA00362223	2026-02-18 02:51:29
1819	2657	email	\N	EFTA00362644	2026-02-18 02:51:29
1820	2658	email	\N	EFTA00968898	2026-02-18 02:51:29
1821	2658	email	\N	EFTA01206030	2026-02-18 02:51:29
1822	2658	email	\N	EFTA00905014	2026-02-18 02:51:29
1823	2658	email	\N	EFTA00384553	2026-02-18 02:51:29
1824	2658	email	\N	EFTA02715990	2026-02-18 02:51:29
1825	2659	email	\N	EFTA01922064	2026-02-18 02:51:29
1826	2659	email	\N	EFTA00904276	2026-02-18 02:51:29
1827	2659	email	\N	EFTA00905741	2026-02-18 02:51:29
1828	2659	email	\N	EFTA00904273	2026-02-18 02:51:29
1829	2659	email	\N	EFTA02396513	2026-02-18 02:51:29
1830	2660	email	\N	EFTA00739819	2026-02-18 02:51:29
1831	2660	email	\N	EFTA00773824	2026-02-18 02:51:29
1832	2660	email	\N	EFTA00765214	2026-02-18 02:51:29
1833	2660	email	\N	EFTA00740824	2026-02-18 02:51:29
1834	2660	email	\N	EFTA00771571	2026-02-18 02:51:29
1835	2661	email	\N	EFTA00861584	2026-02-18 02:51:29
1836	2661	email	\N	EFTA02428903	2026-02-18 02:51:29
1837	2661	email	\N	EFTA00935684	2026-02-18 02:51:29
1838	2661	email	\N	EFTA02512117	2026-02-18 02:51:29
1839	2661	email	\N	EFTA00762672	2026-02-18 02:51:29
1840	2662	email	\N	EFTA00950869	2026-02-18 02:51:29
1841	2662	email	\N	EFTA00321442	2026-02-18 02:51:29
1842	2662	email	\N	EFTA00398774	2026-02-18 02:51:29
1843	2662	email	\N	EFTA00420791	2026-02-18 02:51:29
1844	2662	email	\N	EFTA02175460	2026-02-18 02:51:29
1845	2663	email	\N	EFTA00496408	2026-02-18 02:51:29
1846	2663	email	\N	EFTA00457880	2026-02-18 02:51:29
1847	2663	email	\N	EFTA00353492	2026-02-18 02:51:29
1848	2663	email	\N	EFTA02084178	2026-02-18 02:51:29
1849	2663	email	\N	EFTA02151356	2026-02-18 02:51:29
1850	2664	email	\N	EFTA02191605	2026-02-18 02:51:29
1851	2664	email	\N	EFTA00458938	2026-02-18 02:51:29
1852	2664	email	\N	EFTA00476301	2026-02-18 02:51:29
1853	2664	email	\N	EFTA02234292	2026-02-18 02:51:29
1854	2664	email	\N	EFTA00445294	2026-02-18 02:51:29
1855	2665	email	\N	EFTA02164538	2026-02-18 02:51:29
1856	2665	email	\N	EFTA02165093	2026-02-18 02:51:29
1857	2665	email	\N	EFTA02165614	2026-02-18 02:51:29
1858	2665	email	\N	EFTA02165622	2026-02-18 02:51:29
1859	2665	email	\N	EFTA02137524	2026-02-18 02:51:29
1860	2666	email	\N	EFTA01769486	2026-02-18 02:51:29
1861	2666	email	\N	EFTA01873254	2026-02-18 02:51:29
1862	2666	email	\N	EFTA00877416	2026-02-18 02:51:29
1863	2666	email	\N	EFTA01769872	2026-02-18 02:51:29
1864	2666	email	\N	EFTA00647873	2026-02-18 02:51:29
1865	2667	email	\N	EFTA00906201	2026-02-18 02:51:29
1866	2667	email	\N	EFTA00900707	2026-02-18 02:51:29
1867	2667	email	\N	EFTA02023080	2026-02-18 02:51:29
1868	2667	email	\N	EFTA01836426	2026-02-18 02:51:29
1869	2667	email	\N	EFTA00696648	2026-02-18 02:51:29
1870	2668	email	\N	EFTA00743944	2026-02-18 02:51:29
1871	2668	email	\N	EFTA00697062	2026-02-18 02:51:29
1872	2668	email	\N	EFTA00351232	2026-02-18 02:51:29
1873	2668	email	\N	EFTA00377860	2026-02-18 02:51:29
1874	2668	email	\N	EFTA00651481	2026-02-18 02:51:29
1875	2669	email	\N	EFTA02071569	2026-02-18 02:51:29
1876	2669	email	\N	EFTA00378070	2026-02-18 02:51:29
1877	2669	email	\N	EFTA00394252	2026-02-18 02:51:29
1878	2669	email	\N	EFTA02071232	2026-02-18 02:51:29
1879	2669	email	\N	EFTA02207446	2026-02-18 02:51:29
1880	2670	email	\N	EFTA01888239	2026-02-18 02:51:29
1881	2670	email	\N	EFTA00944734	2026-02-18 02:51:29
1882	2670	email	\N	EFTA01798704	2026-02-18 02:51:29
1883	2670	email	\N	EFTA00404176	2026-02-18 02:51:29
1884	2670	email	\N	EFTA01987495	2026-02-18 02:51:29
1885	2671	email	\N	EFTA02309081	2026-02-18 02:51:29
1886	2671	email	\N	EFTA02344412	2026-02-18 02:51:29
1887	2671	email	\N	EFTA00546190	2026-02-18 02:51:29
1888	2671	email	\N	EFTA00547088	2026-02-18 02:51:29
1889	2671	email	\N	EFTA00547098	2026-02-18 02:51:29
1890	2672	email	\N	EFTA02365520	2026-02-18 02:51:29
1891	2672	email	\N	EFTA02365451	2026-02-18 02:51:29
1892	2672	email	\N	EFTA02659283	2026-02-18 02:51:29
1893	2672	email	\N	EFTA00662368	2026-02-18 02:51:29
1894	2672	email	\N	EFTA02366328	2026-02-18 02:51:29
1895	2673	email	\N	EFTA01029002	2026-02-18 02:51:29
1896	2673	email	\N	EFTA02538032	2026-02-18 02:51:29
1897	2673	email	\N	EFTA01933510	2026-02-18 02:51:29
1898	2673	email	\N	EFTA02627678	2026-02-18 02:51:29
1899	2673	email	\N	EFTA01779382	2026-02-18 02:51:29
1900	2674	email	\N	EFTA01033359	2026-02-18 02:51:29
1901	2674	email	\N	EFTA02666025	2026-02-18 02:51:29
1902	2674	email	\N	EFTA02315733	2026-02-18 02:51:29
1903	2674	email	\N	EFTA00554406	2026-02-18 02:51:29
1904	2674	email	\N	EFTA00554417	2026-02-18 02:51:29
1905	2675	email	\N	EFTA01822727	2026-02-18 02:51:29
1906	2675	email	\N	EFTA00666061	2026-02-18 02:51:29
1907	2675	email	\N	EFTA00649066	2026-02-18 02:51:29
1908	2675	email	\N	EFTA00750567	2026-02-18 02:51:29
1909	2675	email	\N	EFTA02318588	2026-02-18 02:51:29
1910	2676	email	\N	EFTA01200191	2026-02-18 02:51:29
1911	2676	email	\N	EFTA00673195	2026-02-18 02:51:29
1912	2676	email	\N	EFTA00905860	2026-02-18 02:51:29
1913	2676	email	\N	EFTA01200199	2026-02-18 02:51:29
1914	2676	email	\N	EFTA00884660	2026-02-18 02:51:29
1915	2677	email	\N	EFTA01916477	2026-02-18 02:51:29
1916	2677	email	\N	EFTA00677967	2026-02-18 02:51:29
1917	2677	email	\N	EFTA01980272	2026-02-18 02:51:29
1918	2677	email	\N	EFTA01920172	2026-02-18 02:51:29
1919	2677	email	\N	EFTA00874023	2026-02-18 02:51:29
1920	2678	email	\N	EFTA01829009	2026-02-18 02:51:29
1921	2678	email	\N	EFTA02442393	2026-02-18 02:51:29
1922	2678	email	\N	EFTA02458867	2026-02-18 02:51:29
1923	2678	email	\N	EFTA02645293	2026-02-18 02:51:29
1924	2678	email	\N	EFTA02458577	2026-02-18 02:51:29
1925	2679	email	\N	EFTA00859978	2026-02-18 02:51:29
1926	2679	email	\N	EFTA02499356	2026-02-18 02:51:29
1927	2679	email	\N	EFTA02660785	2026-02-18 02:51:29
1928	2679	email	\N	EFTA00864553	2026-02-18 02:51:29
1929	2679	email	\N	EFTA02498478	2026-02-18 02:51:29
1930	2680	email	\N	EFTA01477054	2026-02-18 02:51:29
1931	2680	email	\N	EFTA01472206	2026-02-18 02:51:29
1932	2680	email	\N	EFTA01468805	2026-02-18 02:51:29
1933	2680	email	\N	EFTA01468810	2026-02-18 02:51:29
1934	2680	email	\N	EFTA01474726	2026-02-18 02:51:29
1935	2681	email	\N	EFTA02136334	2026-02-18 02:51:29
1936	2681	email	\N	EFTA02136308	2026-02-18 02:51:29
1937	2681	email	\N	EFTA02136321	2026-02-18 02:51:29
1938	2681	email	\N	EFTA02136565	2026-02-18 02:51:29
1939	2681	email	\N	EFTA02135243	2026-02-18 02:51:29
1940	2682	email	\N	EFTA00370883	2026-02-18 02:51:29
1941	2682	email	\N	EFTA02119699	2026-02-18 02:51:29
1942	2682	email	\N	EFTA02059410	2026-02-18 02:51:29
1943	2682	email	\N	EFTA02059787	2026-02-18 02:51:29
1944	2682	email	\N	EFTA02059759	2026-02-18 02:51:29
1945	2683	email	\N	EFTA02518463	2026-02-18 02:51:29
1946	2683	email	\N	EFTA01739030	2026-02-18 02:51:29
1947	2683	email	\N	EFTA00814205	2026-02-18 02:51:29
1948	2683	email	\N	EFTA02670966	2026-02-18 02:51:29
1949	2683	email	\N	EFTA01063287	2026-02-18 02:51:29
1950	2684	email	\N	EFTA01029667	2026-02-18 02:51:29
1951	2684	email	\N	EFTA00458938	2026-02-18 02:51:29
1952	2684	email	\N	EFTA00458177	2026-02-18 02:51:29
1953	2684	email	\N	EFTA02205067	2026-02-18 02:51:29
1954	2684	email	\N	EFTA00444334	2026-02-18 02:51:29
1955	2685	email	\N	EFTA02644555	2026-02-18 02:51:29
1956	2685	email	\N	EFTA00634757	2026-02-18 02:51:29
1957	2685	email	\N	EFTA02341757	2026-02-18 02:51:29
1958	2685	email	\N	EFTA02623222	2026-02-18 02:51:29
1959	2685	email	\N	EFTA02623187	2026-02-18 02:51:29
1960	2686	email	\N	EFTA00667781	2026-02-18 02:51:29
1961	2686	email	\N	EFTA01933413	2026-02-18 02:51:29
1962	2686	email	\N	EFTA01933286	2026-02-18 02:51:29
1963	2686	email	\N	EFTA01931431	2026-02-18 02:51:29
1964	2686	email	\N	EFTA00711270	2026-02-18 02:51:29
1965	2687	email	\N	EFTA00899441	2026-02-18 02:51:29
1966	2687	email	\N	EFTA00774591	2026-02-18 02:51:29
1967	2687	email	\N	EFTA00712152	2026-02-18 02:51:29
1968	2687	email	\N	EFTA00881565	2026-02-18 02:51:29
1969	2687	email	\N	EFTA00941006	2026-02-18 02:51:29
1970	2688	email	\N	EFTA01861372	2026-02-18 02:51:29
1971	2688	email	\N	EFTA01763304	2026-02-18 02:51:29
1972	2688	email	\N	EFTA02506534	2026-02-18 02:51:29
1973	2688	email	\N	EFTA02515358	2026-02-18 02:51:29
1974	2688	email	\N	EFTA01762879	2026-02-18 02:51:29
1975	2689	email	\N	EFTA00967378	2026-02-18 02:51:29
1976	2689	email	\N	EFTA01966401	2026-02-18 02:51:29
1977	2689	email	\N	EFTA00873390	2026-02-18 02:51:29
1978	2689	email	\N	EFTA01762642	2026-02-18 02:51:29
1979	2689	email	\N	EFTA02573664	2026-02-18 02:51:29
1980	2690	email	\N	EFTA01857408	2026-02-18 02:51:29
1981	2690	email	\N	EFTA01987762	2026-02-18 02:51:29
1982	2690	email	\N	EFTA00915997	2026-02-18 02:51:29
1983	2690	email	\N	EFTA00917459	2026-02-18 02:51:29
1984	2690	email	\N	EFTA00917504	2026-02-18 02:51:29
1985	2691	email	\N	EFTA01589783	2026-02-18 02:51:29
1986	2691	email	\N	EFTA01590816	2026-02-18 02:51:29
1987	2691	email	\N	EFTA01405013	2026-02-18 02:51:29
1988	2691	email	\N	EFTA01769047	2026-02-18 02:51:29
1989	2691	email	\N	EFTA01400939	2026-02-18 02:51:29
1990	2692	email	\N	EFTA00393575	2026-02-18 02:51:29
1991	2692	email	\N	EFTA01055600	2026-02-18 02:51:29
1992	2692	email	\N	EFTA00393573	2026-02-18 02:51:29
1993	2692	email	\N	EFTA00433955	2026-02-18 02:51:29
1994	2692	email	\N	EFTA00439568	2026-02-18 02:51:29
1995	2693	email	\N	EFTA01737944	2026-02-18 02:51:29
1996	2693	email	\N	EFTA02606268	2026-02-18 02:51:29
1997	2693	email	\N	EFTA02607857	2026-02-18 02:51:29
1998	2693	email	\N	EFTA00710987	2026-02-18 02:51:29
1999	2693	email	\N	EFTA00385812	2026-02-18 02:51:29
2000	2694	email	\N	EFTA00391075	2026-02-18 02:51:29
2001	2694	email	\N	EFTA00861082	2026-02-18 02:51:29
2002	2694	email	\N	EFTA00865018	2026-02-18 02:51:29
2003	2694	email	\N	EFTA00709854	2026-02-18 02:51:29
2004	2694	email	\N	EFTA02140214	2026-02-18 02:51:29
2005	2695	email	\N	EFTA02287000	2026-02-18 02:51:29
2006	2695	email	\N	EFTA02077169	2026-02-18 02:51:29
2007	2695	email	\N	EFTA02089587	2026-02-18 02:51:29
2008	2695	email	\N	EFTA02078253	2026-02-18 02:51:29
2009	2695	email	\N	EFTA00572327	2026-02-18 02:51:29
2010	2696	email	\N	EFTA00900707	2026-02-18 02:51:29
2011	2696	email	\N	EFTA01836426	2026-02-18 02:51:29
2012	2696	email	\N	EFTA00696648	2026-02-18 02:51:29
2013	2696	email	\N	EFTA00900630	2026-02-18 02:51:29
2014	2696	email	\N	EFTA02012574	2026-02-18 02:51:29
2015	2697	email	\N	EFTA00954885	2026-02-18 02:51:29
2016	2697	email	\N	EFTA00700778	2026-02-18 02:51:29
2017	2697	email	\N	EFTA01762793	2026-02-18 02:51:29
2018	2697	email	\N	EFTA01973391	2026-02-18 02:51:29
2019	2697	email	\N	EFTA01902917	2026-02-18 02:51:29
2020	2698	email	\N	EFTA02165048	2026-02-18 02:51:29
2021	2698	email	\N	EFTA02338856	2026-02-18 02:51:29
2022	2698	email	\N	EFTA00871210	2026-02-18 02:51:29
2023	2698	email	\N	EFTA01952803	2026-02-18 02:51:29
2024	2698	email	\N	EFTA02078405	2026-02-18 02:51:29
2025	2699	email	\N	EFTA00327660	2026-02-18 02:51:29
2026	2699	email	\N	EFTA00362236	2026-02-18 02:51:29
2027	2699	email	\N	EFTA00362644	2026-02-18 02:51:29
2028	2699	email	\N	EFTA00362223	2026-02-18 02:51:29
2029	2699	email	\N	EFTA00362623	2026-02-18 02:51:29
2030	2700	email	\N	EFTA02064328	2026-02-18 02:51:29
2031	2700	email	\N	EFTA00332464	2026-02-18 02:51:29
2032	2700	email	\N	EFTA02064702	2026-02-18 02:51:29
2033	2700	email	\N	EFTA02064322	2026-02-18 02:51:29
2034	2700	email	\N	EFTA02064472	2026-02-18 02:51:29
2035	2701	email	\N	EFTA00817938	2026-02-18 02:51:29
2036	2701	email	\N	EFTA00818820	2026-02-18 02:51:29
2037	2701	email	\N	EFTA00366373	2026-02-18 02:51:29
2038	2701	email	\N	EFTA00664717	2026-02-18 02:51:29
2039	2701	email	\N	EFTA00817841	2026-02-18 02:51:29
2040	2702	email	\N	EFTA02531843	2026-02-18 02:51:29
2041	2702	email	\N	EFTA00483556	2026-02-18 02:51:29
2042	2702	email	\N	EFTA00476384	2026-02-18 02:51:29
2043	2702	email	\N	EFTA02261918	2026-02-18 02:51:29
2044	2702	email	\N	EFTA00483554	2026-02-18 02:51:29
2045	2703	email	\N	EFTA00540387	2026-02-18 02:51:29
2046	2703	email	\N	EFTA00540876	2026-02-18 02:51:29
2047	2703	email	\N	EFTA00859406	2026-02-18 02:51:29
2048	2703	email	\N	EFTA00716826	2026-02-18 02:51:29
2049	2703	email	\N	EFTA02458800	2026-02-18 02:51:29
2050	2704	email	\N	EFTA02309535	2026-02-18 02:51:29
2051	2704	email	\N	EFTA01773439	2026-02-18 02:51:29
2052	2704	email	\N	EFTA00547918	2026-02-18 02:51:29
2053	2704	email	\N	EFTA02025775	2026-02-18 02:51:29
2054	2704	email	\N	EFTA02002249	2026-02-18 02:51:29
2055	2705	email	\N	EFTA01981567	2026-02-18 02:51:29
2056	2705	email	\N	EFTA00701151	2026-02-18 02:51:29
2057	2705	email	\N	EFTA01777553	2026-02-18 02:51:29
2058	2705	email	\N	EFTA00701411	2026-02-18 02:51:29
2059	2705	email	\N	EFTA00659358	2026-02-18 02:51:29
2060	2706	email	\N	EFTA00736014	2026-02-18 02:51:29
2061	2706	email	\N	EFTA00737561	2026-02-18 02:51:29
2062	2706	email	\N	EFTA00779398	2026-02-18 02:51:29
2063	2706	email	\N	EFTA00758326	2026-02-18 02:51:29
2064	2706	email	\N	EFTA02413952	2026-02-18 02:51:29
2065	2707	email	\N	EFTA00859110	2026-02-18 02:51:29
2066	2707	email	\N	EFTA00819328	2026-02-18 02:51:29
2067	2707	email	\N	EFTA02662470	2026-02-18 02:51:29
2068	2707	email	\N	EFTA02452045	2026-02-18 02:51:29
2069	2707	email	\N	EFTA01051483	2026-02-18 02:51:29
2070	2708	email	\N	EFTA02412984	2026-02-18 02:51:29
2071	2708	email	\N	EFTA01849302	2026-02-18 02:51:29
2072	2708	email	\N	EFTA01779990	2026-02-18 02:51:29
2073	2708	email	\N	EFTA00898616	2026-02-18 02:51:29
2074	2708	email	\N	EFTA01800288	2026-02-18 02:51:29
2075	2709	email	\N	EFTA02420555	2026-02-18 02:51:29
2076	2709	email	\N	EFTA01984336	2026-02-18 02:51:29
2077	2709	email	\N	EFTA01984384	2026-02-18 02:51:29
2078	2709	email	\N	EFTA00924646	2026-02-18 02:51:29
2079	2709	email	\N	EFTA00924092	2026-02-18 02:51:29
2080	2710	email	\N	EFTA01844561	2026-02-18 02:51:29
2081	2710	email	\N	EFTA01844630	2026-02-18 02:51:29
2082	2710	email	\N	EFTA02023180	2026-02-18 02:51:29
2083	2710	email	\N	EFTA02339616	2026-02-18 02:51:29
2084	2710	email	\N	EFTA00928591	2026-02-18 02:51:29
2085	2711	email	\N	EFTA01589048	2026-02-18 02:51:29
2086	2711	email	\N	EFTA01588773	2026-02-18 02:51:29
2087	2711	email	\N	EFTA01588896	2026-02-18 02:51:29
2088	2711	email	\N	EFTA01588763	2026-02-18 02:51:29
2089	2711	email	\N	EFTA01589058	2026-02-18 02:51:29
2090	2712	email	\N	EFTA00324718	2026-02-18 02:51:29
2091	2712	email	\N	EFTA00324721	2026-02-18 02:51:29
2092	2712	email	\N	EFTA00333143	2026-02-18 02:51:29
2093	2712	email	\N	EFTA00333126	2026-02-18 02:51:29
2094	2713	email	\N	EFTA02246493	2026-02-18 02:51:29
2095	2713	email	\N	EFTA00338495	2026-02-18 02:51:29
2096	2713	email	\N	EFTA00474081	2026-02-18 02:51:29
2097	2713	email	\N	EFTA00536569	2026-02-18 02:51:29
2098	2714	email	\N	EFTA00392259	2026-02-18 02:51:29
2099	2714	email	\N	EFTA00958888	2026-02-18 02:51:29
2100	2714	email	\N	EFTA00958882	2026-02-18 02:51:29
2101	2714	email	\N	EFTA00958876	2026-02-18 02:51:29
2102	2715	email	\N	EFTA00649066	2026-02-18 02:51:29
2103	2715	email	\N	EFTA02721277	2026-02-18 02:51:29
2104	2715	email	\N	EFTA00744080	2026-02-18 02:51:29
2105	2715	email	\N	EFTA00750567	2026-02-18 02:51:29
2106	2716	email	\N	EFTA00922432	2026-02-18 02:51:29
2107	2716	email	\N	EFTA02535993	2026-02-18 02:51:29
2108	2716	email	\N	EFTA02408668	2026-02-18 02:51:29
2109	2716	email	\N	EFTA00720037	2026-02-18 02:51:29
2110	2717	email	\N	EFTA00892201	2026-02-18 02:51:29
2111	2717	email	\N	EFTA02413634	2026-02-18 02:51:29
2112	2717	email	\N	EFTA02414027	2026-02-18 02:51:29
2113	2717	email	\N	EFTA00749369	2026-02-18 02:51:29
2114	2718	email	\N	EFTA00814229	2026-02-18 02:51:29
2115	2718	email	\N	EFTA01739473	2026-02-18 02:51:29
2116	2718	email	\N	EFTA00814272	2026-02-18 02:51:29
2117	2718	email	\N	EFTA01739639	2026-02-18 02:51:29
2118	2719	email	\N	EFTA00834636	2026-02-18 02:51:29
2119	2719	email	\N	EFTA00859110	2026-02-18 02:51:29
2120	2719	email	\N	EFTA01051483	2026-02-18 02:51:29
2121	2719	email	\N	EFTA02655276	2026-02-18 02:51:29
2122	2720	email	\N	EFTA02462515	2026-02-18 02:51:29
2123	2720	email	\N	EFTA02703249	2026-02-18 02:51:29
2124	2720	email	\N	EFTA00865078	2026-02-18 02:51:29
2125	2720	email	\N	EFTA02693974	2026-02-18 02:51:29
2126	2721	email	\N	EFTA01855305	2026-02-18 02:51:29
2127	2721	email	\N	EFTA01857172	2026-02-18 02:51:29
2128	2721	email	\N	EFTA00919163	2026-02-18 02:51:29
2129	2721	email	\N	EFTA02036482	2026-02-18 02:51:29
2130	2722	email	\N	EFTA02597179	2026-02-18 02:51:29
2131	2722	email	\N	EFTA02598927	2026-02-18 02:51:29
2132	2722	email	\N	EFTA02596983	2026-02-18 02:51:29
2133	2722	email	\N	EFTA01754301	2026-02-18 02:51:29
2134	2723	email	\N	EFTA00714150	2026-02-18 02:51:29
2135	2723	email	\N	EFTA00339963	2026-02-18 02:51:29
2136	2723	email	\N	EFTA01873966	2026-02-18 02:51:29
2137	2724	email	\N	EFTA00428081	2026-02-18 02:51:29
2138	2724	email	\N	EFTA00368862	2026-02-18 02:51:29
2139	2724	email	\N	EFTA00368928	2026-02-18 02:51:29
2140	2725	email	\N	EFTA02283000	2026-02-18 02:51:29
2141	2725	email	\N	EFTA00369152	2026-02-18 02:51:29
2142	2725	email	\N	EFTA00369155	2026-02-18 02:51:29
2143	2726	email	\N	EFTA02519317	2026-02-18 02:51:29
2144	2726	email	\N	EFTA00379820	2026-02-18 02:51:29
2145	2726	email	\N	EFTA00379826	2026-02-18 02:51:29
2146	2727	email	\N	EFTA00394973	2026-02-18 02:51:29
2147	2727	email	\N	EFTA00433584	2026-02-18 02:51:29
2148	2727	email	\N	EFTA02137524	2026-02-18 02:51:29
2149	2728	email	\N	EFTA01769845	2026-02-18 02:51:29
2150	2728	email	\N	EFTA00412244	2026-02-18 02:51:29
2151	2728	email	\N	EFTA00543281	2026-02-18 02:51:29
2152	2729	email	\N	EFTA00437131	2026-02-18 02:51:29
2153	2729	email	\N	EFTA02190351	2026-02-18 02:51:29
2154	2729	email	\N	EFTA02190381	2026-02-18 02:51:29
2155	2730	email	\N	EFTA00460666	2026-02-18 02:51:29
2156	2730	email	\N	EFTA00461585	2026-02-18 02:51:29
2157	2730	email	\N	EFTA00460661	2026-02-18 02:51:29
2158	2731	email	\N	EFTA01140567	2026-02-18 02:51:29
2159	2731	email	\N	EFTA00651563	2026-02-18 02:51:29
2160	2731	email	\N	EFTA01756668	2026-02-18 02:51:29
2161	2732	email	\N	EFTA00666923	2026-02-18 02:51:29
2162	2732	email	\N	EFTA01038175	2026-02-18 02:51:29
2163	2732	email	\N	EFTA00995524	2026-02-18 02:51:29
2164	2733	email	\N	EFTA01741026	2026-02-18 02:51:29
2165	2733	email	\N	EFTA00687529	2026-02-18 02:51:29
2166	2733	email	\N	EFTA01741006	2026-02-18 02:51:29
2167	2734	email	\N	EFTA01922064	2026-02-18 02:51:29
2168	2734	email	\N	EFTA02396513	2026-02-18 02:51:29
2169	2734	email	\N	EFTA00707011	2026-02-18 02:51:29
2170	2735	email	\N	EFTA02001049	2026-02-18 02:51:29
2171	2735	email	\N	EFTA01831952	2026-02-18 02:51:29
2172	2735	email	\N	EFTA00709083	2026-02-18 02:51:29
2173	2736	email	\N	EFTA01916625	2026-02-18 02:51:29
2174	2736	email	\N	EFTA00720993	2026-02-18 02:51:29
2175	2736	email	\N	EFTA01915599	2026-02-18 02:51:29
2176	2737	email	\N	EFTA00770482	2026-02-18 02:51:29
2177	2737	email	\N	EFTA00884571	2026-02-18 02:51:29
2178	2737	email	\N	EFTA00740185	2026-02-18 02:51:29
2179	2738	email	\N	EFTA02436957	2026-02-18 02:51:29
2180	2738	email	\N	EFTA00770194	2026-02-18 02:51:29
2181	2738	email	\N	EFTA00965704	2026-02-18 02:51:29
2182	2739	email	\N	EFTA01402518	2026-02-18 02:51:29
2183	2739	email	\N	EFTA00844534	2026-02-18 02:51:29
2184	2739	email	\N	EFTA01474803	2026-02-18 02:51:29
2185	2740	email	\N	EFTA02027291	2026-02-18 02:51:29
2186	2740	email	\N	EFTA02028522	2026-02-18 02:51:29
2187	2740	email	\N	EFTA00878785	2026-02-18 02:51:29
2188	2741	email	\N	EFTA00921514	2026-02-18 02:51:29
2189	2741	email	\N	EFTA01853805	2026-02-18 02:51:29
2190	2741	email	\N	EFTA01989970	2026-02-18 02:51:29
2191	2742	email	\N	EFTA01436137	2026-02-18 02:51:29
2192	2742	email	\N	EFTA02005134	2026-02-18 02:51:29
2193	2742	email	\N	EFTA01411821	2026-02-18 02:51:29
2194	2743	email	\N	EFTA02458577	2026-02-18 02:51:29
2195	2743	email	\N	EFTA01785434	2026-02-18 02:51:29
2196	2743	email	\N	EFTA02336631	2026-02-18 02:51:29
2197	2744	email	\N	EFTA00189202	2026-02-18 02:51:29
2198	2744	email	\N	EFTA00214928	2026-02-18 02:51:29
2199	2745	email	\N	EFTA00338657	2026-02-18 02:51:29
2200	2745	email	\N	EFTA02423373	2026-02-18 02:51:29
2201	2746	email	\N	EFTA00353302	2026-02-18 02:51:29
2202	2746	email	\N	EFTA00733360	2026-02-18 02:51:29
2203	2747	email	\N	EFTA02072932	2026-02-18 02:51:29
2204	2747	email	\N	EFTA00353364	2026-02-18 02:51:29
2205	2748	email	\N	EFTA00353713	2026-02-18 02:51:29
2206	2748	email	\N	EFTA02086385	2026-02-18 02:51:29
2207	2749	email	\N	EFTA00359465	2026-02-18 02:51:29
2208	2749	email	\N	EFTA00359467	2026-02-18 02:51:29
2209	2750	email	\N	EFTA00774250	2026-02-18 02:51:29
2210	2750	email	\N	EFTA00370981	2026-02-18 02:51:29
2211	2751	email	\N	EFTA00384070	2026-02-18 02:51:29
2212	2751	email	\N	EFTA02130162	2026-02-18 02:51:29
2213	2752	email	\N	EFTA00429389	2026-02-18 02:51:29
2214	2752	email	\N	EFTA00917539	2026-02-18 02:51:29
2215	2753	email	\N	EFTA00443254	2026-02-18 02:51:29
2216	2753	email	\N	EFTA00442945	2026-02-18 02:51:29
2217	2754	email	\N	EFTA02615143	2026-02-18 02:51:29
2218	2754	email	\N	EFTA00469107	2026-02-18 02:51:29
2219	2755	email	\N	EFTA00478750	2026-02-18 02:51:29
2220	2755	email	\N	EFTA00478582	2026-02-18 02:51:29
2221	2756	email	\N	EFTA00774250	2026-02-18 02:51:29
2222	2756	email	\N	EFTA00629724	2026-02-18 02:51:29
2223	2757	email	\N	EFTA00636933	2026-02-18 02:51:29
2224	2757	email	\N	EFTA00673244	2026-02-18 02:51:29
2225	2758	email	\N	EFTA00697075	2026-02-18 02:51:29
2226	2758	email	\N	EFTA00643937	2026-02-18 02:51:29
2227	2759	email	\N	EFTA00652526	2026-02-18 02:51:29
2228	2759	email	\N	EFTA00962143	2026-02-18 02:51:29
2229	2760	email	\N	EFTA02401235	2026-02-18 02:51:29
2230	2760	email	\N	EFTA00711477	2026-02-18 02:51:29
2231	2761	email	\N	EFTA00718562	2026-02-18 02:51:29
2232	2761	email	\N	EFTA00876016	2026-02-18 02:51:29
2233	2762	email	\N	EFTA00751207	2026-02-18 02:51:29
2234	2762	email	\N	EFTA00751204	2026-02-18 02:51:29
2235	2763	email	\N	EFTA00758534	2026-02-18 02:51:29
2236	2763	email	\N	EFTA02423930	2026-02-18 02:51:29
2237	2764	email	\N	EFTA00763983	2026-02-18 02:51:29
2238	2764	email	\N	EFTA02633022	2026-02-18 02:51:29
2239	2765	email	\N	EFTA01256081	2026-02-18 02:51:29
2240	2765	email	\N	EFTA00773396	2026-02-18 02:51:29
2241	2766	email	\N	EFTA00857900	2026-02-18 02:51:29
2242	2766	email	\N	EFTA00857754	2026-02-18 02:51:29
2243	2767	email	\N	EFTA00878237	2026-02-18 02:51:29
2244	2767	email	\N	EFTA00913831	2026-02-18 02:51:29
2245	2768	email	\N	EFTA01834420	2026-02-18 02:51:29
2246	2768	email	\N	EFTA00902486	2026-02-18 02:51:29
2247	2769	email	\N	EFTA01017946	2026-02-18 02:51:29
2248	2769	email	\N	EFTA01738880	2026-02-18 02:51:29
2249	2770	email	\N	EFTA02660888	2026-02-18 02:51:29
2250	2770	email	\N	EFTA01055196	2026-02-18 02:51:29
2251	2771	email	\N	EFTA02028450	2026-02-18 02:51:29
2252	2771	email	\N	EFTA01773805	2026-02-18 02:51:29
2253	2772	email	\N	EFTA01814389	2026-02-18 02:51:29
2254	2772	email	\N	EFTA02413153	2026-02-18 02:51:29
2255	2773	email	\N	EFTA01905818	2026-02-18 02:51:29
2256	2773	email	\N	EFTA01905937	2026-02-18 02:51:29
2257	2774	email	\N	EFTA01915132	2026-02-18 02:51:29
2258	2774	email	\N	EFTA02167941	2026-02-18 02:51:29
2259	2775	email	\N	EFTA01961765	2026-02-18 02:51:29
2260	2775	email	\N	EFTA01961245	2026-02-18 02:51:29
2261	2776	email	\N	EFTA01964149	2026-02-18 02:51:29
2262	2776	email	\N	EFTA02393868	2026-02-18 02:51:29
2263	2777	email	\N	EFTA02071720	2026-02-18 02:51:29
2264	2777	email	\N	EFTA02071764	2026-02-18 02:51:29
2265	2778	email	\N	EFTA02300458	2026-02-18 02:51:29
2266	2778	email	\N	EFTA02089802	2026-02-18 02:51:29
2267	2779	email	\N	EFTA02147105	2026-02-18 02:51:29
2268	2779	email	\N	EFTA02146610	2026-02-18 02:51:29
2269	2780	email	\N	EFTA02617195	2026-02-18 02:51:29
2270	2780	email	\N	EFTA02617256	2026-02-18 02:51:29
\.


--
-- Data for Name: resolved_identities; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.resolved_identities (id, raw_name, raw_email, canonical_name, person_registry_slug, kg_entity_id, confidence, match_method) FROM stdin;
1853	\N	leevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1854	\N	cjeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1855	\N	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1856	\N	ejeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1857	\N	jeevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1858	\N	leevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1859	\N	lesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	1	email
1860	\N	jeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1861	\N	jeevacation@grnail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1862	\N	cieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1863	\N	cleevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1864	\N	ieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1865	\N	jeevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1866	\N	leevacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1867	\N	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1868	\N	cjeevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1869	\N	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1870	\N	leevacation@grnail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1871	\N	jeevacation@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1872	\N	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1873	\N	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
1874	\N	ijeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1875	\N	evacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1876	\N	jeevacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1877	\N	icevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1878	\N	jcevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1879	\N	jeevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1880	\N	ieevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1881	\N	ieevacation@omail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1882	\N	lcevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1883	\N	ieevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1884	\N	ileevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1885	\N	leevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1886	\N	leevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1887	\N	jeeproject@yahoo.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1888	\N	jjeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1889	\N	eevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1890	\N	cevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1891	\N	ieevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1892	&qu=t;jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1893	&quo=;jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1894	, Amy Dempsey	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1895	, and	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1896	, and > >	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1897	, and destroy this communication and all copies thereof=2C	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1898	, jeffrey epstein Masha, Thank you for the introduction! Jeffrey, It's a pleasure!	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1899	4=xleffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1900	= "Jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1901	= "Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1902	="jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1903	="jeffrey E.&q=ot	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1904	=/b> "Jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1905	=/b> =effrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1906	=/b> =effrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1907	=/b> =effrey Epstein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1908	=/b> Jeffrey =pstein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1909	=/b> Jeffrey =pstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1910	=/b> Jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1911	=/b> Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1912	=/b>"jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1913	=/b>1	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1914	=/b>Ann Rodriquez	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1915	=/b>J	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1916	=/b>Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1917	=/b>Rich Kahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
1918	=/b>Richard Kahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
1919	=/b>Robert Lawrence Kuhn	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1920	=/b>leffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1921	=/span> jeffrey E	jeevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1922	=/span> jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1923	=/span>"jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1924	=1	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1925	==	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1926	=A0Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1927	=AO "Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1928	=AO "Jeffrey Epstein&quo=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1929	=AO please note The information contained in this communication is	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1930	=C2*Richard Kahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
1931	=FSF	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1932	=Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1933	=Karyna Shuliak ear="none" class="yiv7079317862"> Ok On Thu, Oct 11, 2018 at 10:44 AM 1171)	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
1934	=Lesley Groff	lesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	1	email
1935	=b class="">Jeffrey	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1936	=b class="gmail_sendername">jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1937	=com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1938	=effrey	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1939	=effrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1940	=effrey E	evacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1941	=effrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1942	=effrey Epstein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1943	=effrey epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1944	=ffre E	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1945	=ichard Kahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
1946	=ichard Kahn "jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1947	=jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1948	=jeffrey E	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1949	=quot;jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1950	=quotjeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1951	=span style="font-size: 10pe> Jeffrey Epstein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1952	=span style="font-size: 10pt;"> Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1953	=span style="font-size: 10pt;"> Jeffrey Epstein (mailto	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1954	=span style="font-size: l0pe> Jeffrey Epstein imailto	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1955	=span style="font-size: l0pt;"> Jeffrey Epstein (mailto	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1956	=span style="font-size: l0pt;"> jeffrey epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1957	=span style="font-size: lOpt;"> Jeffrey Epstein (mailto	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1958	=span style="font•size: l0pt;"> Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1959	=span style=ifont-size:10.0pe> Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1960	=span style=ifont-size:10.0pe> Jeffrey Epstein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1961	=strong class="gmail_sendername" dir="auto">Richard Kahn =span dir="ltr" class="">	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
1962	=tory	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1963	> Paris 7 November, 2018 Jeffrey -- Many thanks for dinner last night	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1964	>, Jeffrey =pstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1965	>, Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1966	Ada Clapp	\N	\N	ada-clapp	\N	0.9	exact
1967	Ada Clapp	aclapp@elysllc.com	\N	ada-clapp	\N	0.9	exact
1968	Ada Clapp 	\N	\N	ada-clapp	\N	0.9	exact
1969	Al Seckel	\N	Al Seckel	al-seckel	\N	0.9	exact
1970	Al seckel	\N	Al Seckel	al-seckel	\N	0.9	exact
1971	Al seckel	aseckel@yahoo.com	Al Seckel	al-seckel	\N	0.9	exact
1972	Alan Dershowitz	\N	Alan Dershowitz	alan-dershowitz	\N	0.9	exact
1973	Alan Dershowitz	alandersh@gmail.com	Alan Dershowitz	alan-dershowitz	\N	0.9	exact
1974	Alan Dershowitz 	\N	Alan Dershowitz	alan-dershowitz	\N	0.9	exact
1975	Alan Halperin	\N	\N	alan-halperin	\N	0.9	exact
1976	Alan Halperin	halperin@paulweiss.com	\N	alan-halperin	\N	0.9	exact
1977	Alan M. Dershowitz	\N	Alan Dershowitz	alan-dershowitz	\N	0.7	fuzzy
1978	Alan S Halperin	\N	\N	alan-halperin	\N	0.7	fuzzy
1979	Alan S. Halperin	\N	\N	alan-halperin	\N	0.7	fuzzy
1980	Alex Acosta	\N	Alexander Acosta	alexander-acosta	\N	0.9	exact
1981	Alexander Rossmiller	\N	ALEXANDER ROSSMILLER	alexander-rossmiller	\N	0.9	exact
1982	Alireza Ittihadieh	\N	\N	alireza-ittihadieh	\N	0.9	exact
1983	Alireza Ittihadieh	alireza@freestreambermuda.bm	\N	alireza-ittihadieh	\N	0.9	exact
1984	Alison Moe	\N	Alison Moe	alison-moe	\N	0.9	exact
1985	Amanda Kirby	\N	\N	amanda-kirby	\N	0.9	exact
1986	Amanda Kirby	amanda.kirby+external@db.com	\N	amanda-kirby	\N	0.9	exact
1987	Amanda Skarbnik	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1988	Andrew Farkas	\N	Andrew Farkas	andrew-farkas	\N	0.9	exact
1989	Andrew Lourie	andrew.lourie2@usdoj.gov	Andrew Lourie	andrew-lourie	\N	0.9	exact
1990	Andrew Lourie	\N	Andrew Lourie	andrew-lourie	\N	0.9	exact
1991	Andrew Oosterbaan	\N	Andrew Oosterbaan	andrew-oosterbaan	\N	0.9	exact
1992	Ann Rodriguez	\N	Ann Rodriguez	ann-rodriguez	\N	0.9	exact
1993	Ann Rodriqu=z	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
1994	Ann Rodriquez	\N	\N	ann-rodriquez	\N	0.9	exact
1995	Ann Rodriquez	annrodriquez@yahoo.com	\N	ann-rodriquez	\N	0.9	exact
1996	Anthony Barrett	\N	Anthony Barrett	anthony-barrett	\N	0.9	exact
1997	Antoine Verglas	\N	Antoine Verglas	antoine-verglas	\N	0.9	exact
1998	Ariane Dwyer	\N	\N	ariane-dwyer	\N	0.9	exact
1999	Ariane de Rothschild	\N	Ariane de Rothschild	ariane-de-rothschild	\N	0.9	exact
2000	Ashley	\N	Ashley	ashley	\N	0.9	exact
2001	Audrey Strauss	\N	Audrey Strauss	audrey-strauss	\N	0.9	exact
2002	Austin Hill	\N	Austin Hill	austin-hill	\N	0.9	exact
2003	Barbara Burns	\N	Barbara Burns	barbara-burns	\N	0.9	exact
2004	Barnaby Marsh	\N	Barnaby Marsh	barnaby-marsh	\N	0.9	exact
2005	Barnaby Marsh	aby.marsh@gmail.com	Barnaby Marsh	barnaby-marsh	\N	0.9	exact
2006	Barnaby Marsh Bamaby, Joi has meetings all day but the easiest to reschedule would be between 10:30am-3pm. Would something in that time frame work? Should we plan on Joi going to Harvard to meet you and Jeffrey? On Sat, Mar 26, 2016 at 10:15 PM, Joichi Ito wrote: Got it. Heather, can you help? - Joi On Mar 27, 2016, at 6:13 AM, Bamaby Marsh	\N	Barnaby Marsh	barnaby-marsh	\N	0.7	fuzzy
2007	Barry Josephson	\N	Barry Josephson	barry-josephson	\N	0.9	exact
2008	Barry Josephson	barry@jos-ent.com	Barry Josephson	barry-josephson	\N	0.9	exact
2009	Barry Krischer	\N	Barry Krischer	barry-krischer	\N	0.9	exact
2010	Bella Klein	\N	Bella Klein	bella-klein	\N	0.9	exact
2011	Bella Klein	5@gmail.com	Bella Klein	bella-klein	\N	0.9	exact
2012	Bella Klein	bklein575@gmail.com	Bella Klein	bella-klein	\N	0.9	exact
2013	Bella Klein , Jefffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2014	Ben Goertzel	\N	Ben Goertzel	ben-goertzel	\N	0.9	exact
2015	Bill Gates	\N	Bill Gates	bill-gates	\N	0.9	exact
2016	Bobby Kotick	\N	Bobby Kotick	bobby-kotick	\N	0.9	exact
2017	Boris NikoliC	\N	Boris Nikolic	boris-nikolic	\N	0.9	exact
2018	Boris Nikolic	\N	Boris Nikolic	boris-nikolic	\N	0.9	exact
2019	Boris Nikolic	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2020	Boris Nikolic (BGC3)	\N	Boris Nikolic	boris-nikolic	\N	0.9	exact
2021	Boris Nikolic (bgC3)	\N	Boris Nikolic	boris-nikolic	\N	0.9	exact
2022	Boris Nikolic (bgC3)	olic@gatesfoundation.org	Boris Nikolic	boris-nikolic	\N	0.9	exact
2023	Boris Nikolic , Boris Nikolic	\N	Boris Nikolic	boris-nikolic	\N	0.7	fuzzy
2024	Boris Nikolic =ubject: i m at the =anch „ The information contained in this communication is	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2025	Boris Nikolic S=bject: im in paris.= Has bill been in contact with Larry? ••••= The information =ontained in this communication is confidential, may be attorney-client =rivileged, may constitute inside information, and is intended only for	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2026	Boris Nikolic Subject Re: Regina yes„ but i didn't see comfirmation of your email being sent On Mon, Mar 12, 2012 at 9:18 PM, Boris Nikolic	\N	Boris Nikolic	boris-nikolic	\N	0.7	fuzzy
2027	Boris Nikolic=br> Subject: Re: talk today? On Thu, Feb 11, 2016 at 10:55 PM, Boris Nikolic	\N	Boris Nikolic	boris-nikolic	\N	0.7	fuzzy
2028	Brad Edwards	\N	Bradley Edwards	bradley-edwards	\N	0.9	exact
2029	Brad Edwards	brad@eplic.com	Bradley Edwards	bradley-edwards	\N	0.9	exact
2030	Brad Edwards	brad@epllc.com	Bradley Edwards	bradley-edwards	\N	0.9	exact
2031	Brad Edwards	brad@pathtojustice.com	Bradley Edwards	bradley-edwards	\N	0.9	exact
2032	Brad Karp	\N	Brad Karp	brad-karp	\N	0.9	exact
2033	Brad Wechsler	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2034	Brian Vickers	\N	Brian Vickers	brian-vickers	\N	0.9	exact
2035	Brice & Karen Gordon	\N	Brice Gordon	brice-gordon	\N	0.7	fuzzy
2036	Brice Gordon	\N	Brice Gordon	brice-gordon	\N	0.9	exact
2037	Brice Gordon	zdc.rt41@gmail.com	Brice Gordon	brice-gordon	\N	0.9	exact
2038	Brice Gordon	zorro.office@gmail.com	Brice Gordon	brice-gordon	\N	0.9	exact
2039	Brice Gordon its non taxable so no differnce but whatever you prefer On Fri, Dec 23, 2016 at 9:37 AM, Brice Gordon	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2040	Brock Pierce	\N	Brock Pierce	brock-pierce	\N	0.9	exact
2041	Bruce Moskowitz	\N	Bruce Moskowitz	bruce-moskowitz	\N	0.9	exact
2042	Bryan Bishop	\N	Bryan Bishop	bryan-bishop	\N	0.9	exact
2043	CARLUZ TOYLO	\N	Carluz Toylo	carluz-toylo	\N	0.9	exact
2044	CARLUZ TOYLO	zulrac@icloud.com	Carluz Toylo	carluz-toylo	\N	0.9	exact
2045	Captain	\N	CAPTAIN	captain	\N	0.9	exact
2046	Carluz Toylo	\N	Carluz Toylo	carluz-toylo	\N	0.9	exact
2047	Caroline Lang	\N	Caroline Lang	caroline-lang	\N	0.9	exact
2048	Caroline Lang	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2049	Casey Tegreene	\N	Casey Tegreene	casey-tegreene	\N	0.9	exact
2050	Casey Wasserman	\N	Casey Wasserman	casey-wasserman	\N	0.9	exact
2051	Catherine	\N	Catherine	catherine	\N	0.9	exact
2052	Cecile de Jongh	\N	Cecile de Jongh	cecile-de-jongh	\N	0.9	exact
2053	Cecile de Jongh	ceciledejongh@yahoo.com	Cecile de Jongh	cecile-de-jongh	\N	0.9	exact
2054	Cecile de Jongh	ceciledejongh@yahoo.corn	Cecile de Jongh	cecile-de-jongh	\N	0.9	exact
2055	Cecile de Jongh	ceciledeionoh@yahoo.com	Cecile de Jongh	cecile-de-jongh	\N	0.9	exact
2056	Chris Kroblin	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2057	Clare Probert	\N	\N	clare-probert	\N	0.9	exact
2058	Claudia Leschuck	\N	\N	claudia-leschuck	\N	0.9	exact
2059	Claudia leschuck	\N	\N	claudia-leschuck	\N	0.9	exact
2060	Cynthia Rodriguez	\N	\N	cynthia-rodriguez	\N	0.9	exact
2061	Cynthia Rodriguez	cynthia.rodriguez@db.com	\N	cynthia-rodriguez	\N	0.9	exact
2062	DAVID MITCHELL	\N	David Mitchell	david-mitchell	\N	0.9	exact
2063	Dan Ariely	\N	Dan Ariely	dan-ariely	\N	0.9	exact
2064	Dana	\N	Dana	dana	\N	0.9	exact
2065	Daniel Sabba	\N	\N	daniel-sabba	\N	0.9	exact
2066	Daniel Siad	\N	Daniel Siad	daniel-siad	\N	0.9	exact
2067	Danielle	\N	Danielle	danielle	\N	0.9	exact
2068	Danny Hillis	\N	Danny Hillis	danny-hillis	\N	0.9	exact
2069	Danny Vicars	\N	Danny Vicars	danny-vicars	\N	0.9	exact
2070	Danny Vicars	dannyvicars@yahoo.com	Danny Vicars	danny-vicars	\N	0.9	exact
2071	Daphne Wallace	\N	Daphne Wallace	daphne-wallace	\N	0.9	exact
2072	Daphne Wallace	dlbwallace@gmail.com	Daphne Wallace	daphne-wallace	\N	0.9	exact
2073	Daphne Wallace	rinacic@interfreight-cargo.com	Daphne Wallace	daphne-wallace	\N	0.9	exact
2074	Daphne Wallace	dlbwallace@gmall.com	Daphne Wallace	daphne-wallace	\N	0.9	exact
2075	Daphne Wallace	clibwallace@gmall.com	Daphne Wallace	daphne-wallace	\N	0.9	exact
2076	Daphne Wallace	dlbwallace@gmail.co	Daphne Wallace	daphne-wallace	\N	0.9	exact
2077	Daphne Wallace	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2078	Daphne Wallace >, Jeanne Brennan	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2079	Darren INDYKE	\N	Darren Indyke	darren-indyke	\N	0.9	exact
2080	Darren Indyke	\N	Darren Indyke	darren-indyke	\N	0.9	exact
2081	Darren Indyke	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2082	Darren Indyke	dkiesq@aol.com	Darren Indyke	darren-indyke	\N	0.9	exact
2083	Darren K Indyke	\N	Darren Indyke	darren-indyke	\N	0.7	fuzzy
2084	Darren K. Indyke	\N	Darren K. Indyke	darren-k-indyke	\N	0.9	exact
2085	Darren indyke	\N	Darren Indyke	darren-indyke	\N	0.9	exact
2086	David Boies	\N	David Boies	david-boies	\N	0.9	exact
2087	David David Mitchell	\N	David Mitchell	david-mitchell	\N	0.7	fuzzy
2088	David Koch	\N	David Koch	david-koch	\N	0.9	exact
2089	David Mitchell	\N	David Mitchell	david-mitchell	\N	0.9	exact
2090	David Mitchell	djm@mitchellholdings.com	David Mitchell	david-mitchell	\N	0.9	exact
2091	David Mitchell" , "Oliver Mitchell	\N	David Mitchell	david-mitchell	\N	0.7	fuzzy
2092	David Mitchell" a, "Oliver Mitchell	\N	David Mitchell	david-mitchell	\N	0.7	fuzzy
2093	David Schoen	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2094	David Stern	\N	David Stern	david-stern	\N	0.9	exact
2095	Dear Richard Kahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
2096	Deborah Pechet Quinan	\N	\N	deborah-pechet-quinan	\N	0.9	exact
2097	Deepak Chopra	\N	Deepak Chopra	deepak-chopra	\N	0.9	exact
2098	Deepak Chopra	nonlocal101@chopra.com	Deepak Chopra	deepak-chopra	\N	0.9	exact
2099	Derrick	\N	Derrick	derrick	\N	0.9	exact
2100	Detective FAX COVER SHEET FAX: Palm Beach Police Department If you have any questions or need anything else, please contact me at Number of pages including this page 2	\N	Detective 2	detective-2	\N	0.7	fuzzy
2101	Detective FAX COVER SHEET FAX: Palm Beach Police Department rm If you have any questions or need anything else, please contact me at Number of pages including this page 2	\N	Detective 2	detective-2	\N	0.7	fuzzy
2102	Dick Cavett	\N	Dick Cavett	dick-cavett	\N	0.9	exact
2103	Doug	\N	Doug	doug	\N	0.9	exact
2104	Doug	darnaudin@mitchellholdings.com	Doug	doug	\N	0.9	exact
2105	Doug Band	\N	Doug Band	doug-band	\N	0.9	exact
2106	Doug Schoettle	\N	Doug Schoettle	doug-schoettle	\N	0.9	exact
2107	Dr. Henr Jarecki	\N	Dr. Jarecki	dr-jarecki	\N	0.7	fuzzy
2108	Dr. Henry Jarecki	\N	Dr. Jarecki	dr-jarecki	\N	0.7	fuzzy
2109	Dr. Jarecki	\N	Dr. Jarecki	dr-jarecki	\N	0.9	exact
2110	Dr. Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2111	E. jeffrey	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2112	Ehud Barak	\N	Ehud Barak	ehud-barak	\N	0.9	exact
2113	Eileen Alex	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2114	Eileen Alexanderson	\N	\N	eileen-alexanderson	\N	0.9	exact
2115	Eileen Alexanderson	ealexanderson@apollo-advisors.com	\N	eileen-alexanderson	\N	0.9	exact
2116	Eileen Guggenheim	\N	Eileen Guggenheim	eileen-guggenheim	\N	0.9	exact
2117	Elon Musk	\N	Elon Musk	elon-musk	\N	0.9	exact
2118	Emad Hanna	\N	Emad Hanna	emad-hanna	\N	0.9	exact
2119	Emad Hanna	ehanna@hbrkassociates.com	Emad Hanna	emad-hanna	\N	0.9	exact
2120	Envoye de mon iPhone Debut du message transfers : Expediteur: 3BIS Fabrice BOURG <	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2121	Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2122	Epstein Jeffrey	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2123	Er=ka Kellerhals	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2124	Eric Roth	\N	\N	eric-roth	\N	0.9	exact
2125	Eric Roth	eroth@intljet.com	\N	eric-roth	\N	0.9	exact
2126	Eric Roth	hn12@gmail.com	\N	eric-roth	\N	0.9	exact
2127	Eric Roth =b>Subject	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2128	Eric Roth St:Oct: =u> http://www.edm=stoncompany.com/luxury-yachts-for-sale/alfa-nero-9/	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2129	Eric Roth St=ject: =u> http://www.edm=stoncompany.com/luxury-yachts-for-sale/alfa-nero-9/	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2130	Eric Roth jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2131	Erika Kellerhal ubject: Re: Did we agree you deserve to =e happy. you were going to check with bill and get bck to me , =ut didnt. I m ok with whatver you find fair On Wed, May =0, 2018 at 1:53 PM Erika Kellerhals	\N	Erika Kellerhals	erika-kellerhals	\N	0.7	fuzzy
2132	Erika Kellerhals	\N	Erika Kellerhals	erika-kellerhals	\N	0.9	exact
2133	Erika Kellerhals	ekellerhals@kfficlaw.com	Erika Kellerhals	erika-kellerhals	\N	0.9	exact
2134	Erika Kellerhals	ekellerhals@kellfer.com	Erika Kellerhals	erika-kellerhals	\N	0.9	exact
2135	Erika Kellerhals	rhals@kellfer.com	Erika Kellerhals	erika-kellerhals	\N	0.9	exact
2136	Erika Kellerhals	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2137	Erika Kellerhals	ekellerhals@kffldaw.com	Erika Kellerhals	erika-kellerhals	\N	0.9	exact
2138	Erika Kellerhals	ekellerhals@kffklaw.com	Erika Kellerhals	erika-kellerhals	\N	0.9	exact
2139	Erika Kellerhals	hals@kellfer.com	Erika Kellerhals	erika-kellerhals	\N	0.9	exact
2140	Erika Kellerhals	ellerhals@kffklaw.com	Erika Kellerhals	erika-kellerhals	\N	0.9	exact
2141	Eva Dubin	\N	Eva Dubin	eva-dubin	\N	0.9	exact
2142	For the invoice, could you precise : Name of the Client Adress of facturation Many thanks & see you soon for the project	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2143	Gary Kerney	\N	Gary Kerney	gary-kerney	\N	0.9	exact
2144	Gary Kerney	gkemey@landmarklandco.com	Gary Kerney	gary-kerney	\N	0.9	exact
2145	Gary Kerney	gkerney@landmarklandco.com	Gary Kerney	gary-kerney	\N	0.9	exact
2146	Geoffrey Berman	\N	Geoffrey Berman	geoffrey-berman	\N	0.9	exact
2147	George Church	\N	George Church	george-church	\N	0.9	exact
2148	George Stephanopoulos	\N	George Stephanopoulos	george-stephanopoulos	\N	0.9	exact
2149	Gerald Ja Sussman	\N	Gerald Sussman	gerald-sussman	\N	0.7	fuzzy
2150	Gerald Lefcourt	\N	Gerald Lefcourt	gerald-lefcourt	\N	0.9	exact
2151	Ghislaine Maxwell	\N	Ghislaine Maxwell	ghislaine-maxwell	\N	0.9	exact
2152	Gino Yu y E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2153	Glenn Dubin	\N	Glenn Dubin	glenn-dubin	\N	0.9	exact
2154	Gmax	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2155	Greg Wyler	\N	Greg Wyler	greg-wyler	\N	0.9	exact
2156	Greg Wyler	grot@crowhurst.ws	Greg Wyler	greg-wyler	\N	0.9	exact
2157	Guy Lewis	\N	Guy Lewis	guy-lewis	\N	0.9	exact
2158	Harry Beller	\N	Harry Beller	harry-beller	\N	0.9	exact
2159	Harry Fisch	\N	Harry Fisch	harry-fisch	\N	0.9	exact
2160	Hi Eva, This is the contact info I found for Dr. Eiss, doctor	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2161	Howard Lutnick	\N	Howard Lutnick	howard-lutnick	\N	0.9	exact
2162	I Jep	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2163	I removed the cliches On Mon, Oct 3, 2011 at 10:42 PM, Jeffrey Epstein	ieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2164	Ian Ian Maxwell	ircmaxwell@gmail.com	Ian Maxwell	ian-maxwell	\N	0.7	fuzzy
2165	Ike Groff	\N	\N	ike-groff	\N	0.9	exact
2166	Ion Nicola	\N	\N	ion-nicola	\N	0.9	exact
2167	Isabel Maxwell	\N	Isabel Maxwell	lady-ghislaine	\N	0.9	exact
2168	Ivjet=br>Subject	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2169	Ivjet=br>Subject	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2170	J E n	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2171	J Jep	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2172	J=ffrey	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2173	J=ffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2174	J=ffrey Epstein (mailto:jeevacation=gmail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2175	JE Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2176	JE Jail	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2177	JEE	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2178	JEFFREY EPSTEIN	\N	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2179	JEFFREY EPSTEIN	jepstein02@snet.net	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2180	Jack Horner	\N	Jack Horner	jack-horner	\N	0.9	exact
2181	Jack Scarola	\N	Jack Scarola	jack-scarola	\N	0.9	exact
2182	Jacob Rothschild	\N	Jacob Rothschild	jacob-rothschild	\N	0.9	exact
2183	James Petrucci	\N	James Petrucci	james-petrucci	\N	0.9	exact
2184	Janusz Banasiak	\N	Janusz Banasiak	janusz-banasiak	\N	0.9	exact
2185	Janusz Banasiak	janusz53@me.com	Janusz Banasiak	janusz-banasiak	\N	0.9	exact
2186	Jay Lefkowitz	\N	Jay Lefkowitz	jay-lefkowitz	\N	0.9	exact
2187	Jay Lefkowitz	leficowitz@kirkland.com	Jay Lefkowitz	jay-lefkowitz	\N	0.9	exact
2188	Jay Lefkowitz	jlefkowitz@kirkland.com	Jay Lefkowitz	jay-lefkowitz	\N	0.9	exact
2189	Je vacation	jeevacation@grnail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2190	Je vacation	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2191	Je=frey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2192	Jean Luc Brunel	\N	Jean Luc Brunel	jean-luc-brunel	\N	0.9	exact
2193	Jean Luc Brunel	2jeanluc@gmail.com	Jean Luc Brunel	jean-luc-brunel	\N	0.9	exact
2194	Jeanne	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2195	Jeanne Brennan	\N	\N	jeanne-brennan	\N	0.9	exact
2196	Jeanne Brennan Wiebracht	\N	Jeanne Brennan Wiebracht	jeanne-brennan-wiebracht	\N	0.9	exact
2197	Jeannine Jeskewitz	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2198	Jeevacation	ieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2199	Jeevacation	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2200	Jeevacation	jeevacation@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2201	Jeevacation	jeevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2202	Jeevacation	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2203	Jeevacation	icevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2204	Jeevacation	jeevacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2205	Jeevacation	jcevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2206	Jef=rey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2207	Jeff	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2208	Jeff Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2209	Jeff Sloman	\N	Jeff Sloman	jeff-sloman	\N	0.9	exact
2210	Jeff=ey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2211	Jeff=ey Epstein	evacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2212	Jeff=ey Epstein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2213	Jeffe Edwards	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2214	Jeffey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2215	Jefffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2216	Jefffrey Epstein	ieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2217	Jefffrey Epstein	jeevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2218	Jeffre	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2219	Jeffre E stein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2220	Jeffre E stein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2221	Jeffre E stein 'eevacation .gmail.com)	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2222	Jeffre= Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2223	Jeffre= Epstein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2224	Jeffre= Epstein	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2225	Jeffrey	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2226	Jeffrey	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2227	Jeffrey	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2228	Jeffrey / E / Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2229	Jeffrey / e / Epstein	\N	Jeffrey Epstein	jeffrey-epstein	\N	0.7	fuzzy
2230	Jeffrey / e I Epstein	\N	Jeffrey Epstein	jeffrey-epstein	\N	0.7	fuzzy
2231	Jeffrey =	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2232	Jeffrey = Epstein	mailtojeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.7	fuzzy
2233	Jeffrey =pstein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2234	Jeffrey =pstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2235	Jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2236	Jeffrey E	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2237	Jeffrey E	jeevacation@grnail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2238	Jeffrey E	jeevacation@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2239	Jeffrey E	jeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2240	Jeffrey E	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2241	Jeffrey E	jeevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2242	Jeffrey E	jcevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2243	Jeffrey E	jeevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2244	Jeffrey E	ieevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2245	Jeffrey E	jeevacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2246	Jeffrey E	jeevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2247	Jeffrey E	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2248	Jeffrey E	evacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2249	Jeffrey E ein	eevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2250	Jeffrey E in	eevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2251	Jeffrey E in	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2252	Jeffrey E stein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2253	Jeffrey E." 8	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2254	Jeffrey E."=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2255	Jeffrey E.&quo=	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2256	Jeffrey E.=quot	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2257	Jeffrey E=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2258	Jeffrey E=stein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2259	Jeffrey EPSTEIN	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2260	Jeffrey Ep=tein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2261	Jeffrey Ep=tein	evacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2262	Jeffrey Eps=ein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2263	Jeffrey Eps=ein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2264	Jeffrey Epste=n	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2265	Jeffrey Epstei=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2266	Jeffrey Epstein	\N	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2267	Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2268	Jeffrey Epstein	jeevacation@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2269	Jeffrey Epstein	jeeyacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2270	Jeffrey Epstein	jeevacation@grnail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2271	Jeffrey Epstein	jeevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2272	Jeffrey Epstein	jeeation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2273	Jeffrey Epstein	jeevacation@ginail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2274	Jeffrey Epstein	mailtoleevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2275	Jeffrey Epstein	maittoleev-acation@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2276	Jeffrey Epstein	jeevs@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2277	Jeffrey Epstein	jeevacation@gmaii.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2278	Jeffrey Epstein	jetott@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2279	Jeffrey Epstein	mailtojeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2280	Jeffrey Epstein	jeevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2281	Jeffrey Epstein	jeeyacation@grnail.corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2282	Jeffrey Epstein	malltoleemcation@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2283	Jeffrey Epstein	jeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2284	Jeffrey Epstein	jeeisiott@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2285	Jeffrey Epstein	jeevacation@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2286	Jeffrey Epstein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2287	Jeffrey Epstein	jeesioti@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2288	Jeffrey Epstein	jeea@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2289	Jeffrey Epstein	os@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2290	Jeffrey Epstein	mailtmjeeyacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2291	Jeffrey Epstein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2292	Jeffrey Epstein	mailtmjeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2293	Jeffrey Epstein	mailtoieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2294	Jeffrey Epstein	mailtmjeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2295	Jeffrey Epstein	at@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2296	Jeffrey Epstein	jetos@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2297	Jeffrey Epstein	jettos@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2298	Jeffrey Epstein	jetros@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2299	Jeffrey Epstein	jeta@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2300	Jeffrey Epstein	jeevacalion@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2301	Jeffrey Epstein	jeeat@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2302	Jeffrey Epstein	jeess@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2303	Jeffrey Epstein	jeevacation@gmarl.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2304	Jeffrey Epstein	jeeia@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2305	Jeffrey Epstein	jeevacation@qmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2306	Jeffrey Epstein	jeeyacation@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2307	Jeffrey Epstein	jeevacatton@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2308	Jeffrey Epstein	jetios@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2309	Jeffrey Epstein	jetium@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2310	Jeffrey Epstein	jeeyacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2311	Jeffrey Epstein	jetoti@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2312	Jeffrey Epstein	ios@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2313	Jeffrey Epstein	jetios@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2314	Jeffrey Epstein	jettalos@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2315	Jeffrey Epstein	jeevacation@xmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2316	Jeffrey Epstein	malltoleevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2317	Jeffrey Epstein	mailtoleeyacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2318	Jeffrey Epstein	maittoleevacalion@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2319	Jeffrey Epstein	ation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2320	Jeffrey Epstein	jeevaeation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2321	Jeffrey Epstein	jeevacation@gmall.corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2322	Jeffrey Epstein	jeesios@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2323	Jeffrey Epstein	jesies@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2324	Jeffrey Epstein	jeensium@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2325	Jeffrey Epstein	jeeyacation@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2326	Jeffrey Epstein	jeevacation@gmail.eom	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2327	Jeffrey Epstein	jettm@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2328	Jeffrey Epstein	jeeyacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2329	Jeffrey Epstein	ieevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2330	Jeffrey Epstein	on@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2331	Jeffrey Epstein	jecvacationt@gynail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2332	Jeffrey Epstein	jeesa@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2333	Jeffrey Epstein	jemainti@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2334	Jeffrey Epstein	mailto-jeevacation@gmail.eom	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2335	Jeffrey Epstein	jecvacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2336	Jeffrey Epstein	jccvacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2337	Jeffrey Epstein	jetiuti@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2338	Jeffrey Epstein	malltoleevacation@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2339	Jeffrey Epstein	jeealoti@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2340	Jeffrey Epstein	jeevacation@gmad.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2341	Jeffrey Epstein	jetoti@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2342	Jeffrey Epstein	jeealps@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2343	Jeffrey Epstein	jetius@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2344	Jeffrey Epstein	jeemcatiori@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2345	Jeffrey Epstein	tion@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2346	Jeffrey Epstein	malitmjeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2347	Jeffrey Epstein	jenctin@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2348	Jeffrey Epstein	malitccjeeyacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2349	Jeffrey Epstein	jeea@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2350	Jeffrey Epstein	jeevacation@smaii.corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2351	Jeffrey Epstein	malitoleeracation@gmall.00rn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2352	Jeffrey Epstein	mailtoleevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2353	Jeffrey Epstein	jeevacation@cimail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2354	Jeffrey Epstein	jea@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2355	Jeffrey Epstein	mailtoleevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2356	Jeffrey Epstein	jeevacation@gnnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2357	Jeffrey Epstein	malitoleevacation@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2358	Jeffrey Epstein	jeevacation@zgmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2359	Jeffrey Epstein	jeevacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2360	Jeffrey Epstein	jecvacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2361	Jeffrey Epstein	ieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2362	Jeffrey Epstein	mailtoleevacation@amail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2363	Jeffrey Epstein	jeevacation@rmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2364	Jeffrey Epstein	leevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2365	Jeffrey Epstein	leevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2366	Jeffrey Epstein	ion@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2367	Jeffrey Epstein	on@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2368	Jeffrey Epstein	jeevacation@gmail.comcmailto	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2369	Jeffrey Epstein	n@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2370	Jeffrey Epstein	joevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2371	Jeffrey Epstein	revacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2372	Jeffrey Epstein	joevacation@gmail.comi	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2373	Jeffrey Epstein	jeevacation@qmail..corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2374	Jeffrey Epstein	mailtoueevacation@gmail.c4m	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2375	Jeffrey Epstein	mailtoiecvacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2376	Jeffrey Epstein	mailtotieevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2377	Jeffrey Epstein	jcevacation@email.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2378	Jeffrey Epstein	mailtojecwacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2379	Jeffrey Epstein	ieevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2380	Jeffrey Epstein	jeevacation@nmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2381	Jeffrey Epstein	ietvacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2382	Jeffrey Epstein	jecvacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2383	Jeffrey Epstein	ieevacation@umail.comi	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2384	Jeffrey Epstein	mailtoicevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2385	Jeffrey Epstein	acation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2386	Jeffrey Epstein	jeeyacation@ernail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2387	Jeffrey Epstein	jeevacation@amail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2388	Jeffrey Epstein	jeevacation@kanail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2389	Jeffrey Epstein	jeevacation@ama0.com1	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2390	Jeffrey Epstein	jcevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2391	Jeffrey Epstein	ieevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2392	Jeffrey Epstein	jeevacation@iamail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2393	Jeffrey Epstein	mailtoleevacation@jrnail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2394	Jeffrey Epstein	jeevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2395	Jeffrey Epstein	leevacation@cimail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2396	Jeffrey Epstein	ieevacation@amail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2397	Jeffrey Epstein	teevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2398	Jeffrey Epstein	mailtoleevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2399	Jeffrey Epstein	jeevacation@gmail.eotn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2400	Jeffrey Epstein	mailtmjeeyacation@amail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2401	Jeffrey Epstein	jeevacation@gmail.conl	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2402	Jeffrey Epstein	jeevacation@email.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2403	Jeffrey Epstein	jeevacation@cimail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2404	Jeffrey Epstein	jeevacation@fernall.corni	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2405	Jeffrey Epstein	mailtoileevacation@amail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2406	Jeffrey Epstein	jeeyacation@gmail.o3m	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2407	Jeffrey Epstein	ieevacation@.gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2408	Jeffrey Epstein	rnailtoicevacation@grpail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2409	Jeffrey Epstein	jeeyacation@gmail.comi	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2410	Jeffrey Epstein	ieevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2411	Jeffrey Epstein	ieeyacation@omail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2412	Jeffrey Epstein	ieeyacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2413	Jeffrey Epstein	jecvacation@qpmil.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2414	Jeffrey Epstein	ieevacation@omail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2415	Jeffrey Epstein	jeeyacation@gmail.corni	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2416	Jeffrey Epstein	jeevacation@ernail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2417	Jeffrey Epstein	ieevacation@amail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2418	Jeffrey Epstein	jeevacation@ernall.comi	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2419	Jeffrey Epstein	jeeyacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2420	Jeffrey Epstein	mailtoleeyacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2421	Jeffrey Epstein	jeevacation@gmail.wm	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2422	Jeffrey Epstein	leevacabon@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2423	Jeffrey Epstein	mailtojeevacation@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2424	Jeffrey Epstein	ieeyacation@oinail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2425	Jeffrey Epstein	mailtoleevacation@email.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2426	Jeffrey Epstein	jcevacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2427	Jeffrey Epstein	teevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2428	Jeffrey Epstein	mailtoicevacation@tmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2429	Jeffrey Epstein	jecvacation@email.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2430	Jeffrey Epstein	jeevacation@gmail.con	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2431	Jeffrey Epstein	mailtoueevacation@imail.com1	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2432	Jeffrey Epstein	ieeyacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2433	Jeffrey Epstein	jeeyacation@cimail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2434	Jeffrey Epstein	mailtoleevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2435	Jeffrey Epstein	rnailtoltxvacation@gmail.comi	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2436	Jeffrey Epstein	jeevacation@_gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2437	Jeffrey Epstein	ieevacation@email.comj	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2438	Jeffrey Epstein	jeevacation@gmail.cotn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2439	Jeffrey Epstein	ieeyacation@amail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2440	Jeffrey Epstein	jeeyacation@gmail.coni	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2441	Jeffrey Epstein	jeeyacation@igmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2442	Jeffrey Epstein	ieevacation@amail.arn1	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2443	Jeffrey Epstein	teevaeation@nmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2444	Jeffrey Epstein	jecvacation@mail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2445	Jeffrey Epstein	mailtowevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2446	Jeffrey Epstein	jeeyacation@email.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2447	Jeffrey Epstein	lesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	1	email
2448	Jeffrey Epstein	jeevacation@umail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2449	Jeffrey Epstein	jeevacabon@ornail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2450	Jeffrey Epstein	jeevacation@amail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2451	Jeffrey Epstein	jeevacation@omail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2452	Jeffrey Epstein	jeevacation@gmail.00m	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2453	Jeffrey Epstein	jeevacation@qmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2454	Jeffrey Epstein	jetvacation@gmail.cont	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2455	Jeffrey Epstein	ation@gmail.comi	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2456	Jeffrey Epstein	jeevacation@gmai..com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2457	Jeffrey Epstein	jeevacation@gmail.comi	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2458	Jeffrey Epstein	ntailtoucevacation@gmad.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2459	Jeffrey Epstein	jeevacation@gmail.corni	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2460	Jeffrey Epstein	ieevacation@ornail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2461	Jeffrey Epstein	jeevacation@gmail.00rn	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2462	Jeffrey Epstein	jovacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2463	Jeffrey Epstein	mailtmieevaeation@email.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2464	Jeffrey Epstein	icevacation@email.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2465	Jeffrey Epstein	matitoaecvacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2466	Jeffrey Epstein	ieevaeation@gmail.eom	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2467	Jeffrey Epstein	mailtmeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2468	Jeffrey Epstein	jeevacation@gtnail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2469	Jeffrey Epstein	mmitcnieevaeatton@gmall.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2470	Jeffrey Epstein	jeevacatlon@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2471	Jeffrey Epstein	jeevacation@lmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2472	Jeffrey Epstein	theevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2473	Jeffrey Epstein	mailloaeevacatio.n@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2474	Jeffrey Epstein	rnalitojeevcation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2475	Jeffrey Epstein	jcevacation@gmail.eom	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2476	Jeffrey Epstein	cvmlijeevacation@gmail.comi	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2477	Jeffrey Epstein	jeevacation@gmail.co	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2478	Jeffrey Epstein	hrefemailtoieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2479	Jeffrey Epstein	mailtoleevacation@gmail.cornj	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2480	Jeffrey Epstein (ceva ca tion ma i COM)	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2481	Jeffrey Epstein (jeevacationPgmail.com)	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2482	Jeffrey Epstein (jeevacation®gmail.corn)	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2483	Jeffrey Epstein (mailto	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2484	Jeffrey Epstein .eevaca ion mail com)	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2485	Jeffrey Epstein CC	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2486	Jeffrey Epstein I	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2487	Jeffrey Epstein Imailto	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2488	Jeffrey Epstein Office Jeffrey Epstein	\N	Jeffrey Epstein	jeffrey-epstein	\N	0.7	fuzzy
2489	Jeffrey Epstein beevacation®gmail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2490	Jeffrey Epstein imarlto:jeevacation=gmail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2491	Jeffrey Epstein"=	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2492	Jeffrey Epstein=	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2493	Jeffrey Epstein=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2494	Jeffrey Epstein=	eevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2495	Jeffrey Epstein=cjeevacation=gmail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2496	Jeffrey I	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2497	Jeffrey epstein	\N	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2498	Jeffrey epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2499	Jeffrey epstein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2500	Jeffrey epstein	malltoleevacation@gmall.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2501	Jeffrey epstein	jeevacation@gmail.con1	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2502	Jeffrey epstein	jeevacation@rmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2503	Jeffrey epstein	jeeyacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2504	Jeffrey=/b>	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2505	Jeffrey=Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2506	Jennie Saunders	\N	Jennie Saunders	jennie-saunders	\N	0.9	exact
2507	Jes Staley	\N	Jes Staley	jes-staley	\N	0.9	exact
2508	Jes Staley schedule for week of 25 On Sun, Mar 15, 2015 at 8:07 PM Jes Staley	\N	Jes Staley	jes-staley	\N	0.7	fuzzy
2509	Jes Staley schedule for week of 25 On Sun, Mar 15, 2015 at 8:07 PM, Jes Staley	\N	Jes Staley	jes-staley	\N	0.7	fuzzy
2510	Jesse	\N	Jesse	jesse	\N	0.9	exact
2511	Jesse	iesse@fit4ward.club	Jesse	jesse	\N	0.9	exact
2512	Jj Litchford	\N	\N	jj-litchford	\N	0.9	exact
2513	Jj Litchford	jj.litchford@db.com	\N	jj-litchford	\N	0.9	exact
2514	John Brockman	\N	John Brockman	john-brockman	\N	0.9	exact
2515	John Brockman	broclanan@edge.org	John Brockman	john-brockman	\N	0.9	exact
2516	John Brockman	brockman@edge.org	John Brockman	john-brockman	\N	0.9	exact
2517	John Paulson	\N	John Paulson	john-paulson	\N	0.9	exact
2518	John de Jongh	\N	John de Jongh	john-de-jongh	\N	0.9	exact
2519	Joi Ito	\N	Joi Ito	joi-ito	\N	0.9	exact
2520	Joichi (Joi) Ito	\N	Joi Ito	joi-ito	\N	0.7	fuzzy
2521	Joichi Ito	\N	Joi Ito	joi-ito	\N	0.9	exact
2522	Joichi Ito	joi@media.mit.edu	Joi Ito	joi-ito	\N	0.9	exact
2523	Joichi Joi Ito. Joichi (Joi) Ito	\N	Joi Ito	joi-ito	\N	0.7	fuzzy
2524	Joichi Joi Ito• Joichi (Joi) Ito	\N	Joi Ito	joi-ito	\N	0.7	fuzzy
2525	Joseph L. Ackerman, Jr	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2526	Josh Harris	\N	Josh Harris	josh-harris	\N	0.9	exact
2527	Julia	\N	Julia	julia	\N	0.9	exact
2528	KarYna Shuliak	\N	Karyna Shuliak	karyna-shuliak	\N	0.9	exact
2529	Karyna Shuliak	\N	Karyna Shuliak	karyna-shuliak	\N	0.9	exact
2530	Karyna Shuliak	karynashuliak@icloud.com	Karyna Shuliak	karyna-shuliak	\N	0.9	exact
2531	Karyna Shuliak	thesaintjames.group@gmail.com	Karyna Shuliak	karyna-shuliak	\N	0.9	exact
2532	Karyna Shuliak	kari.shulia@gmail.com	Karyna Shuliak	karyna-shuliak	\N	0.9	exact
2533	Kathryn Ruemmler	\N	Kathryn Ruemmler	kathryn-ruemmler	\N	0.9	exact
2534	Kathy Ruemmler	\N	Kathryn Ruemmler	kathryn-ruemmler	\N	0.9	exact
2535	Kathy Ruemmler	kathvruemmler@gmail.com	Kathryn Ruemmler	kathryn-ruemmler	\N	0.9	exact
2536	Kathy Ruemmler	kathyruemmler@gmail.com	Kathryn Ruemmler	kathryn-ruemmler	\N	0.9	exact
2537	Katie Couric	\N	Katie Couric	katie-couric	\N	0.9	exact
2538	Ken Starr	\N	Kenneth Starr	kenneth-starr	\N	0.9	exact
2539	Kevin Maxwell	\N	Kevin Maxwell	kevin-maxwell	\N	0.9	exact
2540	Kevin Maxwell	maxwellpartners@gmail.com	Kevin Maxwell	kevin-maxwell	\N	0.9	exact
2541	Kimbal Musk	\N	Kimbal Musk	kimbal-musk	\N	0.9	exact
2542	Kimbal Musk	kimbal@thekitchencommunity.org	Kimbal Musk	kimbal-musk	\N	0.9	exact
2543	LAwrence Krauss	\N	Lawrence Krauss	lawrence-krauss	\N	0.9	exact
2544	Larry Cohen	\N	\N	larry-cohen	\N	0.9	exact
2545	Larry Morrison	\N	Larry Morrison	larry-morrison	\N	0.9	exact
2546	Larry Page	\N	Larry Page	larry-page	\N	0.9	exact
2547	Larry Summers	\N	Larry Summers	larry-summers	\N	0.9	exact
2548	Larry Summers	larry@lawrencesummers.com	Larry Summers	larry-summers	\N	0.9	exact
2549	Larry Visoski	\N	Larry Visoski	larry-visoski	\N	0.9	exact
2550	Larry Visoski	lvjet@aol.com	Larry Visoski	larry-visoski	\N	0.9	exact
2551	Larry Visoski	ivjet@aol.com	Larry Visoski	larry-visoski	\N	0.9	exact
2552	Laura A. Menninger	\N	Laura Menninger	laura-menninger	\N	0.7	fuzzy
2553	Laura Menninger	\N	Laura Menninger	laura-menninger	\N	0.9	exact
2554	Laura Menninger	imenninger@hmflaw.com	Laura Menninger	laura-menninger	\N	0.9	exact
2555	Laura Menninger	imenninper@hmflaw.com	Laura Menninger	laura-menninger	\N	0.9	exact
2556	Laurie Edelstein	\N	Laurie Edelstein	laurie-edelstein	\N	0.9	exact
2557	Lawrence Henry Summers	\N	Larry Summers	larry-summers	\N	0.9	exact
2558	Lawrence Krauss	\N	Lawrence Krauss	lawrence-krauss	\N	0.9	exact
2559	Lawrence Krauss	ikrauss@asu.edu	Lawrence Krauss	lawrence-krauss	\N	0.9	exact
2560	Lawrence Krauss	lawkrauss@gmail.com	Lawrence Krauss	lawrence-krauss	\N	0.9	exact
2561	Lawrence Krauss	lawrence.krauss@asu.edu	Lawrence Krauss	lawrence-krauss	\N	0.9	exact
2562	Lawrence Krauss >, Richard Kahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
2563	Lawrence Krauss I On Behalf Of Lawrence Krauss	\N	Lawrence Krauss	lawrence-krauss	\N	0.7	fuzzy
2564	Lawrence Krauss On Behalf Of Lawrence Krauss	\N	Lawrence Krauss	lawrence-krauss	\N	0.7	fuzzy
2565	Lawrence Krauss Professor Krauss	\N	Lawrence Krauss	lawrence-krauss	\N	0.7	fuzzy
2566	Lawrence Krauss • Dear Professor Krauss	\N	Lawrence Krauss	lawrence-krauss	\N	0.7	fuzzy
2567	Lawrence Visoski	\N	Larry Visoski	larry-visoski	\N	0.9	exact
2568	Leon Black	\N	Leon Black	leon-black	\N	0.9	exact
2569	Leon Botstein	\N	Leon Botstein	leon-botstein	\N	0.9	exact
2570	Lesley = Groff	\N	Lesley Groff	lesley-groff	\N	0.7	fuzzy
2571	Lesley =roff	lesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	1	email
2572	Lesley Groff	\N	Lesley Groff	lesley-groff	\N	0.9	exact
2573	Lesley Groff	04419865-9d44-4a9c-ba61-958420f82837@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2574	Lesley Groff	jeeyacation@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2575	Lesley Groff	b5e5b8e9-31b1-45a5-8676-7ada47ae4600@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2576	Lesley Groff	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2577	Lesley Groff	58eee9491d94314d82ef7d3d3d172f4aa63dfe@bfd-maill.nh.local	Lesley Groff	lesley-groff	\N	0.9	exact
2578	Lesley Groff	lesleyjee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2579	Lesley Groff	lesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	1	email
2580	Lesley Groff	t@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2581	Lesley Groff	leslev.jee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2582	Lesley Groff	leslev.iee@omail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2583	Lesley Groff	lesley.iee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2584	Lesley Groff	lesley.iee@ornail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2585	Lesley Groff	mailtolesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2586	Lesley Groff	igroff@dkipllc.com	Lesley Groff	lesley-groff	\N	0.9	exact
2587	Lesley Groff	lesley.jee@gmail.corn	Lesley Groff	lesley-groff	\N	0.9	exact
2588	Lesley Groff	leslcv.jec@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2589	Lesley Groff	leslev.iee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2590	Lesley Groff	ieslev.iee@mmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2591	Lesley Groff	lesleylee@qmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2592	Lesley Groff	lesleyjce@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2593	Lesley Groff	lesley.lee@gmail.conl	Lesley Groff	lesley-groff	\N	0.9	exact
2594	Lesley Groff	lesleyjee@gmail.corn	Lesley Groff	lesley-groff	\N	0.9	exact
2595	Lesley Groff	mailtolesleyjee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2596	Lesley Groff	mailtodesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2597	Lesley Groff	lesley.jee@omail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2598	Lesley Groff	leslevjee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2599	Lesley Groff	mailtodesley.jee@gmail.corn	Lesley Groff	lesley-groff	\N	0.9	exact
2600	Lesley Groff	iesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2601	Lesley Groff	lesiev.iee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2602	Lesley Groff	jee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2603	Lesley Groff	lesleydee@gmail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2604	Lesley Groff	leslev.iee@amail.com	Lesley Groff	lesley-groff	\N	0.9	exact
2605	Lesley Groff	igroff@dkiplic.com	Lesley Groff	lesley-groff	\N	0.9	exact
2606	Lesley Groff 	\N	Lesley Groff	lesley-groff	\N	0.9	exact
2607	Lesley Groff Ike Groff	\N	Lesley Groff	lesley-groff	\N	0.7	fuzzy
2608	Lesley Groff have them find an airine ask On Fri, Mar 9, 2018 at 4:16 PM, Lesley Groff	\N	Lesley Groff	lesley-groff	\N	0.7	fuzzy
2609	Lesley Groff pay from foudntiaon On Fri, Dec 26, 2014 at 1:31 PM, Lesley Groff	\N	Lesley Groff	lesley-groff	\N	0.7	fuzzy
2610	Lesley Groff yes , and then have Egive them to to send On Fri, Feb 1, 2013 at 3:20 PM, Lesley Groff	\N	Lesley Groff	lesley-groff	\N	0.7	fuzzy
2611	Lesley Groff yes On Wed, Aug 22, 2018 at 1:27 PM, Lesley Groff	\N	Lesley Groff	lesley-groff	\N	0.7	fuzzy
2612	Lesley Groff ‹ > This is the invoice Envoye de mon iPhone Le 29 mai 2017 a 17:26, Lesley Groff	\N	Lesley Groff	lesley-groff	\N	0.7	fuzzy
2613	Lesley r i Groff	\N	Lesley Groff	lesley-groff	\N	0.7	fuzzy
2614	Liam Osullivan	\N	\N	liam-osullivan	\N	0.9	exact
2615	Liam Osullivan	liam.osullivan@db.com	\N	liam-osullivan	\N	0.9	exact
2616	Lisa Randall	\N	Lisa Randall	lisa-randall	\N	0.9	exact
2617	Lisa Randall	m@physics.harvard.edu	Lisa Randall	lisa-randall	\N	0.9	exact
2618	Lloyd Blankfein	\N	Lloyd Blankfein	lloyd-blankfein	\N	0.9	exact
2619	MARK TRAMO	\N	Mark Tramo	mark-tramo	\N	0.9	exact
2620	MICHAEL SALNICK	\N	Michael Salnick	michael-salnick	\N	0.9	exact
2621	Marc Rowan	\N	Marc Rowan	marc-rowan	\N	0.9	exact
2622	Marc Rowan	rowan@apollo1p.com	Marc Rowan	marc-rowan	\N	0.9	exact
2623	Mark Epstein	\N	Mark Epstein	mark-epstein	\N	0.9	exact
2624	Mark Jude Tramo	\N	Mark Tramo	mark-tramo	\N	0.9	exact
2625	Mark L Epstein	\N	Mark Epstein	mark-epstein	\N	0.7	fuzzy
2626	Mark L. Epstein	\N	Mark Epstein	mark-epstein	\N	0.7	fuzzy
2627	Mark LLOYD	\N	Mark Lloyd	mark-lloyd	\N	0.9	exact
2628	Mark Lloyd	\N	Mark Lloyd	mark-lloyd	\N	0.9	exact
2629	Mark S. Cohen	\N	Mark Cohen	mark-cohen	\N	0.7	fuzzy
2630	Mark Tramo	\N	Mark Tramo	mark-tramo	\N	0.9	exact
2631	Mark Tramo	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2632	Mark Tramo	jeevacation@jgmail.com	Mark Tramo	mark-tramo	\N	0.9	exact
2633	Martin G Weinberg	\N	Martin Weinberg	martin-weinberg	\N	0.7	fuzzy
2634	Martin G. Weinberg	\N	Martin Weinberg	martin-weinberg	\N	0.7	fuzzy
2635	Martin G. Weinberg	owlmcb@att.net	Martin Weinberg	martin-weinberg	\N	0.7	fuzzy
2636	Martin Nowak	\N	Martin Nowak	martin-nowak	\N	0.9	exact
2637	Martin Nowak	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2638	Martin Weinberg	\N	Martin Weinberg	martin-weinberg	\N	0.9	exact
2639	Martin Weinberg	owlmgw@att.net	Martin Weinberg	martin-weinberg	\N	0.9	exact
2640	Martin Zeman	\N	\N	martin-zeman	\N	0.9	exact
2641	Martin Zeman	martin.zeman@db.com	\N	martin-zeman	\N	0.9	exact
2642	Marvin Minsky	\N	Marvin Minsky	marvin-minsky	\N	0.9	exact
2643	Mary E Erdoes	\N	Mary Erdoes	mary-erdoes	\N	0.7	fuzzy
2644	Mary Erdoes	\N	Mary Erdoes	mary-erdoes	\N	0.9	exact
2645	Masha Drokova	\N	Masha Drokova	masha-drokova	\N	0.9	exact
2646	Matthew I. Menchel	\N	Matthew I. Menchel	matthew-i-menchel	\N	0.9	exact
2647	Maurene Comey	\N	Maurene Comey	maurene-comey	\N	0.9	exact
2648	Max Kohlenberg	\N	\N	max-kohlenberg	\N	0.9	exact
2649	McCaffrey, Carlyn	jcevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2650	Melanie Spinella	\N	\N	melanie-spinella	\N	0.9	exact
2651	Melissa	\N	MeLiSsA	melissa	\N	0.9	exact
2652	Merwin Dela Cruz "Richard Kahn ( r	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
2653	Michael Jackson	\N	Michael Jackson	michael-jackson	\N	0.9	exact
2654	Michael Ovitz	\N	Michael Ovitz	michael-ovitz	\N	0.9	exact
2655	Michael Wolff	\N	Michael Wolff	michael-wolff	\N	0.9	exact
2656	Michelle	\N	Michelle	michelle	\N	0.9	exact
2657	Miroslav LaJcak	\N	Miroslav Lajcak	miroslav-lajcak	\N	0.9	exact
2658	Miroslav Lajcak	\N	Miroslav Lajcak	miroslav-lajcak	\N	0.9	exact
2659	Ms. Ghislaine Maxwell	\N	Ms. Maxwell	ms-maxwell	\N	0.7	fuzzy
2660	Nadia «. href=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2661	Nathan Myhrvold	\N	Nathan Myhrvold	nathan-myhrvold	\N	0.9	exact
2662	Nathan Wolfe	\N	Nathan Wolfe	nathan-wolfe	\N	0.9	exact
2663	Nicholas RIbIs	\N	Nicholas Ribis	nicholas-ribis	\N	0.9	exact
2664	Nicholas Ribis	\N	Nicholas Ribis	nicholas-ribis	\N	0.9	exact
2665	Nicole Junkermann	\N	Nicole Junkermann	nicole-junkermann	\N	0.9	exact
2666	Nicole Simmons	\N	Nicole Simmons	nicole-simmons	\N	0.9	exact
2667	Noam Chomsk , Valeria Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.7	fuzzy
2668	Noam Chomsk Hello Mr. Katz, >, Valeria Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.7	fuzzy
2669	Noam Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.9	exact
2670	Noam Chomsky	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2671	Noam Chomsky	chomsky@mit.edu	Noam Chomsky	noam-chomsky	\N	0.9	exact
2672	Noam Chomsky	chomsky2@mit.edu	Noam Chomsky	noam-chomsky	\N	0.9	exact
2673	Noam Chomsky	ky3@gmail.com	Noam Chomsky	noam-chomsky	\N	0.9	exact
2674	Noam Chomsky	nchomsky3@gmail.com	Noam Chomsky	noam-chomsky	\N	0.9	exact
2675	Noam Chomsky	nchomsky3@gmail.co	Noam Chomsky	noam-chomsky	\N	0.9	exact
2676	Noam Chomsky 	\N	Noam Chomsky	noam-chomsky	\N	0.9	exact
2677	Noam Chomsky =aleria Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.7	fuzzy
2678	Noam Chomsky >, Valeria Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.7	fuzzy
2679	Noam Chomsky C	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2680	Noam Chomsky Id leave it On Sun, Oct 14, 2018 at 5:40 PM Noam Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.7	fuzzy
2681	Noam Chomsky This is a letter that would make the insurance co . Nervous. If it were to be released ., so make it strong On Sat, Oct 13, 2018 at 11:09 AM Noam Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.7	fuzzy
2682	Noam Chomsky phone anytime face to face thrid week in sept > On Mon, Aug 28, 2017 at 9:16 PM, Noam Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.7	fuzzy
2683	Noam Chomsky • n Sat, May 19, 2018 at 2:26 PM, Noam Chomsky	\N	Noam Chomsky	noam-chomsky	\N	0.7	fuzzy
2684	PETER FENWICK	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2685	PETER MANDELSON	\N	Peter Mandelson	peter-mandelson	\N	0.9	exact
2686	PETER MANDELSON	ktouandelson@btintemet.com	Peter Mandelson	peter-mandelson	\N	0.9	exact
2687	PETER MANDELSON Su=ject: Re: yes , you should go to new york for a weekend„ i have been consista=t on this, dddo not lose the opportunity, coming across people you really =njoy is rare - don't be lazy get on a plane On Wed Ma 27 2009 at 7:38 AM, PETER MANDELSON	\N	Peter Mandelson	peter-mandelson	\N	0.7	fuzzy
2688	Paris 7 November, 2018 Jeffrey -- Many thanks for dinner last night	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2689	Paul Barrett	\N	\N	paul-barrett	\N	0.9	exact
2690	Paul Barrett	paul@alphagroupcapital.com	\N	paul-barrett	\N	0.9	exact
2691	Paul Barrett 	\N	\N	paul-barrett	\N	0.9	exact
2692	Paul Cassell	\N	Paul Cassell	paul-cassell	\N	0.9	exact
2693	Paul Cassell	cassellp@law.utah.edu	Paul Cassell	paul-cassell	\N	0.9	exact
2694	Paul Cassell	cassellp_@law.utah.edu	Paul Cassell	paul-cassell	\N	0.9	exact
2695	Paul G. Cassell	\N	Paul Cassell	paul-cassell	\N	0.7	fuzzy
2696	Paul Morris	\N	Paul Morris	paul-morris	\N	0.9	exact
2697	Paul S Barrett	\N	\N	paul-barrett	\N	0.7	fuzzy
2698	Peggy Siegal	\N	Peggy Siegal	peggy-siegal	\N	0.9	exact
2699	Peggy Siegal	pegevsiegal@gmail.com	Peggy Siegal	peggy-siegal	\N	0.9	exact
2700	Peggy Siegal	peggy@peggysiegal.com	Peggy Siegal	peggy-siegal	\N	0.9	exact
2701	Peter Attia	\N	Peter Attia	peter-attia	\N	0.9	exact
2702	Peter Mandelson	\N	Peter Mandelson	peter-mandelson	\N	0.9	exact
2703	Peter Mandelson	p.mandelson@global-counsel.co.uk	Peter Mandelson	peter-mandelson	\N	0.9	exact
2704	Peter Skinner	\N	Peter Skinner	peter-skinner	\N	0.9	exact
2705	Peter Thiel	\N	Peter Thiel	peter-thiel	\N	0.9	exact
2706	Philip Barden	\N	Philip Barden	philip-barden	\N	0.9	exact
2707	Reid Hoffman	\N	Reid Hoffman	reid-hoffman	\N	0.9	exact
2708	Reid Hoffman	rhoffman@greylock.com	Reid Hoffman	reid-hoffman	\N	0.9	exact
2709	Reid Hoffman	rhoffinan@greylock.com	Reid Hoffman	reid-hoffman	\N	0.9	exact
2710	Reid Weingarten	\N	Reid Weingarten	reid-weingarten	\N	0.9	exact
2711	Rich Kahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
2712	Rich Kahn	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2713	Richard =ahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
2714	Richard Axel	\N	Richard Axel	richard-axel	\N	0.9	exact
2715	Richard Branson	\N	Richard Branson	richard-branson	\N	0.9	exact
2716	Richard Branson	roaer.b@virain.com	Richard Branson	richard-branson	\N	0.9	exact
2717	Richard Branson	roger.b@virgin.com	Richard Branson	richard-branson	\N	0.9	exact
2718	Richard Joslin	\N	Richard Joslin	richard-joslin	\N	0.9	exact
2719	Richard Joslin	rjoslin@elyslic.com	Richard Joslin	richard-joslin	\N	0.9	exact
2720	Richard Joslin	r.loslin@elyslic.com	Richard Joslin	richard-joslin	\N	0.9	exact
2721	Richard Joslin 	\N	Richard Joslin	richard-joslin	\N	0.9	exact
2722	Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.9	exact
2723	Richard Kahn	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2724	Richard Kahn	nchardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	0.9	exact
2725	Richard Kahn	mailtorichardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	0.9	exact
2726	Richard Kahn	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
2727	Richard Kahn	bradley.gillin@db.com	Richard Kahn	richard-kahn	\N	0.9	exact
2728	Richard Kahn	richardkahnl2@gmail.com	Richard Kahn	richard-kahn	\N	0.9	exact
2729	Richard Kahn	richarddavidkahn@yahoo.com	Richard Kahn	richard-kahn	\N	0.9	exact
2730	Richard Kahn	richardkahnl2@cimail.com	Richard Kahn	richard-kahn	\N	0.9	exact
2731	Richard Kahn	richardkahn12@ornail.com	Richard Kahn	richard-kahn	\N	0.9	exact
2732	Richard Kahn	richardkahn12@omail.com	Richard Kahn	richard-kahn	\N	0.9	exact
2733	Richard Kahn	ekellerhals@kellfer.com	Richard Kahn	richard-kahn	\N	0.9	exact
2734	Richard Kahn	richardkahn12@gmai..com	Richard Kahn	richard-kahn	\N	0.9	exact
2735	Richard Kahn , Jeffrey Epstein	jeeyacation@gmail.com	Richard Epstein	richard-epstein	\N	0.7	fuzzy
2736	Richard Kahn 10 On Mon, Mar 20, 2017 at 9:21 AM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2737	Richard Kahn 1230 On Wed, =ec 9, 2015 at 10:15 AM, Richard Kahn wrote: a bit to late as i have a =eeting at 1:15pm can do 12:30 or 3:00pm Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2738	Richard Kahn 16 th I lam for thud one way wash best On Thursday, September 10, 2015, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2739	Richard Kahn 16th 11am for ehud one way wash =ost On Thursday, =eptember 10, 2015, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2740	Richard Kahn > Is it complex or finish work DAVID MITCHELL Mitchell Holdings LLC 745 Fifth Avenue New York NY 10151 USA 1212-4864444 On Apr 26, 2018, at 12:01 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2741	Richard Kahn >, Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2742	Richard Kahn Absolutely. When is a good time for me to call? Thank you, James Ce, your Personal Genius, http://personalgenius.us On May 10, 2017, at 2:16 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2743	Richard Kahn Arsenal. They were hired by Premier Sent from Yahoo Mail for iPhone On Friday, June 28, 2019, 1:06 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2744	Richard Kahn Asa On Mon, Jan 29, 2018 at 6:22 PM Richard Kahn wrotc: do you have a time preference for speaking with gary tomorrow please advise thank you Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2745	Richard Kahn Ask Lesley On Mon, Jan 29, 2018 at 6:22 PM Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2746	Richard Kahn Ask On Mon, Jan 29, 2018 at 6:22 PM Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2747	Richard Kahn Ask On Mon, Jan 29, 2018 at 6:22 PM Richard Kahn wrote: do you have a time preference for speaking with gary tomorrow please advise thank you Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2748	Richard Kahn Dear Mr, Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2749	Richard Kahn Good evening Mr. Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2750	Richard Kahn Here is what we can do , not to use middle garage instead use both sides cos' we have 2 Suburbans, we can extend to 24"-30" if we want to without using middle spot. Thanks Carluz Toylo Palm Beach FL. 33480 On Sep 26, 2018, at 17:51, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2751	Richard Kahn Hi Rich, Trying to get ready, I think he can start on Monday Sent from my iPhone On May 30, 2014, at 12:50 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2752	Richard Kahn Hotels in Shanghai: 1) Swissotel grand Shanghai 2) delight Palace Jingan service apartment 3) The Puli hotel and spa 4) Yan'an hotel 5) Pei Mansion hotel II mercoledi 22 luglio 2015, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2753	Richard Kahn I'm sure we can make that work. Are you or jeffrey available later today to discuss Sent from my iPhone On Aug 1, 2016, at 9:06 AM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2754	Richard Kahn If I can talk to Bella in Russian actually =ill be good! On Wednesday, February 18, =015, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2755	Richard Kahn Is it complex or finish work DAVID MITCHELL Mitchell Holdings LLC 745 Fifth Avenue New York NY 10151 USA On Apr 26, 2018, at 12:01 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2756	Richard Kahn Is it complex or finish work DAVID MITCHELL Mitchell Holdings LLC On Apr 26, 2018, at 12:01 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2757	Richard Kahn Sun On Thu, Sep 28, 2017 at 2:40 PM Richard Kahn > wrote: please confirm karluz to NYC this weekend (sat or sun?) also you mentioned apt at 301 to stay at instead of at 9 cast 71st? please advise thank you Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2758	Richard Kahn Sun On Thu, Sep 28, 2017 at 2:40 PM Richard Kahn Ivrote: please confirm karluz to NYC this weekend (sat or sun?) also you mentioned apt at 301 to stay at instead of at 9 east 71st? please advise thank you Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2759	Richard Kahn Thank you again Sent from my iPhone On Feb 22, 2018, at 8:55 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2760	Richard Kahn Thought I responded, apologize if I did not, it has been very intense lately getting these TCOs As I no longer have project managers in any of these projects and doing it myself I advanced all but $50,000 of the investor note payable I am sending you the entire drop box where all the details of payments and advances are found DAVID MITCHELL Mitchell Holdings LLC 745 Fifth Avenue New York NY 10151 USA On May 17, 2018, at 9:18 AM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2761	Richard Kahn Yes On Wednesday, June 17, 2015, Richard Kahn wrote: any interest in meeting with Moshe on Friday? please advise thank you Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2762	Richard Kahn ` =1 Sent: Wednesday Jul 19 2017 10:41 AM ' s Ribis c: je rey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2763	Richard Kahn c-1- 1---"--1-- 4nr‘---" ---% hotel On Wed, Sep 10, 2014 at 11:06 AM, Richard Kahn •I IIM> wrote: ok thank you sam's place or hotel (150 per night cost) Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2764	Richard Kahn do it On The, Sep 16, 2014 at 1:50 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2765	Richard Kahn either , ask larry for same remote in theatre Isj or bed room palm beach ipad is the worst On Wed, Jun 10, 2015 at 2:07 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2766	Richard Kahn hotel On Wed, Sep 10, 2014 at 11.06 AM, Richard Kahn wrote: ok thank you sam's place or hotel (150 per night cost) Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2767	Richard Kahn hotel On Wed, Sep 10, 2014 at 11:06 AM, Richard Kahn wrote: ok thank you sam's place or hotel (150 per night cost) Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2768	Richard Kahn hotel On Wed, Sep 10, 2014 at 11:06 AM, Richard Kahn › wrote: ok thank you sam's place or hotel (150 per night cost) Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2769	Richard Kahn ica was in touch with gardeners about this Sent from my iPhone On Aug 31, 2016, at 6:17 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2770	Richard Kahn ok On Thu, May 4, 2017 at 4:02 PM, Richard Kahn was able to reduce 5178.20 to 4717.66 for 460.54 savings or 8.9% discount please advise if ok to proceed thank you Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2771	Richard Kahn remind me feb On Thu, Jan 24, 2019 at 11:28 PM Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2772	Richard Kahn so make it 20 this year. and the balance next On Fri, Dec 9, 2016 at 12:10 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2773	Richard Kahn tbx On Mon, Dec 14, 2015 at 9:11 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2774	Richard Kahn tc ) Thank you again Sent from my iPhone On Feb 22, 2018, at 8:55 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2775	Richard Kahn thx On Mon, Dec 14, 2015 at 9:11 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2776	Richard Kahn view first On Tue, Nov 10, 2015 at 8:20 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2777	Richard Kahn view first On Tue, Nov 10, 2015 at 8:20 PM, Richard Kahn wrote: Janusz confirmed paver job was completed today Total job cost was 9000 We gave a 5000 deposit Is it ok to make final payment of 4000 or do you want to view before we pay Please advise Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2778	Richard Kahn yes including additional repeater On Fri, Jun 22, 2018 at 12:36 PM, Richard Kahn wrote: Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2779	Richard Kahn «= href="mailto target="_blank" LearJet 60 N114BD Is Blackdiamond S=nt from my iPhone 2014, at 5:1= PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2780	Richard Kahn • Me lysine refund coordinate with her On Thursday, 8 September 2016, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2781	Richard Kahn • c i will be in palm from 28-sept 2 / most of sept free, of course she can go anyday i am not in residence, but be aware i can show up later this week On Tue, Aug 11, 2015 at 8:08 AM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2782	Richard Kahn • i think it should be On Wed, Sep 26, 2018 at 2:07 PM, Richard Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2783	Richard Parsons	\N	Richard Parsons	richard-parsons	\N	0.9	exact
2784	Richard ar Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2785	Richard ati Kahn	\N	Richard Kahn	richard-kahn	\N	0.7	fuzzy
2786	Richard com>	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
2787	Robert Glassman	\N	ROBERT GLASSMAN	robert-glassman	\N	0.9	exact
2788	Robert Lawrence Kuhn	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2789	Robert Trivers	\N	Robert Trivers	robert-trivers	\N	0.9	exact
2790	Robert Y. Lewis	\N	Robert Y. Lewis	robert-y-lewis	\N	0.9	exact
2791	Rodriquez	\N	Alfredo Rodriguez	alfredo-rodriguez	\N	0.9	exact
2792	Rosemary Vrablic	\N	Rosemary Vrablic	rosemary-vrablic	\N	0.9	exact
2793	Roy BLACK	\N	Roy Black	roy-black	\N	0.9	exact
2794	Roy Black	\N	Roy Black	roy-black	\N	0.9	exact
2795	SC=I X-MAIL-FROM	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2796	Sample? Sorry for all the typos .Sent from my iP=one On Jun 3, 2011, at 6:01 PM, ion nicola wrote: hi jeffrey, ..so for the relax room I will do white on white venetian plaster vertical and horizontal lines. w= discussed in new york about making the lines wider. the relax room=has tiles on the floor and one tile is 16X16 inches, so I was thinking to follow th= floor lines up on the wall so those vertical and horizontal lines I will do on th= wall will be 16 inches wide with a distance between them by 16 inches. =3B so we will have somehow the same squares on the wall	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2797	Sara	\N	Sara	sara	\N	0.9	exact
2798	Send to valdson wrote: On Tuesday, 15 November 2016, wrote: Rich has identified 2-3 laptops for Wandi.. still waiting on more feedback from James. OK to ask for Wandi's address to send it to? On Nov 13, 2016, at 11:06 AM, jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2799	Sent: Saturday, April 21, 20=2 3:55 AM	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2800	Shanson900 I asked the chef sorry - begged him to stay on for 4 weeks We have a document of 50 items to shut down a restaurant- ALAN reviewed all items that would be needed to stay in business - don't understand why you keep asking about this - I'm trying my best to have mike stay He had a direct meeting with DAVID on his compensation What's the issue in setting the chef up so he can take over - no different then all the info I have sent DAVID prior to even having the chef think about staying Sent from my iPad On Apr 29, 2018, at 6:26 PM, jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2801	Sigrid McCawley	smccawley_@bsfilp.com	Sigrid McCawley	sigrid-mccawley	\N	0.9	exact
2802	Sigrid McCawley	\N	Sigrid McCawley	sigrid-mccawley	\N	0.9	exact
2803	Skype this week...I'm back in nyc tomorrow, and there unt=I friday On Mon, Jun 26, 20=7 at 8:48 AM jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2804	Soon-Yi Previn	\N	Soon-Yi Previn	soon-yi-previn	\N	0.9	exact
2805	Stephen Kosslyn	\N	Stephen Kosslyn	stephen-kosslyn	\N	0.9	exact
2806	Stephen M Kosslyn	\N	Stephen Kosslyn	stephen-kosslyn	\N	0.7	fuzzy
2807	Stephen M. Kosslyn	\N	Stephen Kosslyn	stephen-kosslyn	\N	0.7	fuzzy
2808	Stephen M. Kosslyn	kosslyn@harvard.edu	Stephen Kosslyn	stephen-kosslyn	\N	0.7	fuzzy
2809	Steve Bannon	\N	Steve Bannon	steve-bannon	\N	0.9	exact
2810	Steve Bannon	steve@arc-ent.com	Steve Bannon	steve-bannon	\N	0.9	exact
2811	Steve Bannon	ve@arc-ent.com	Steve Bannon	steve-bannon	\N	0.9	exact
2812	Steve Hanson	\N	\N	steve-hanson	\N	0.9	exact
2813	Steve Hanson	sohanson@brguestinc.com	\N	steve-hanson	\N	0.9	exact
2814	Steve Hanson Subject• Re• Chess Set hmmmm, I don't know! Let me ask Sarah and Sue...they might know something! On Fri, Jul 13, 2012 at 1:44 PM, Steve Hanson	\N	\N	steve-hanson	\N	0.7	fuzzy
2815	Steve Hanson •e > SulYect: St hen Hanson	\N	\N	steve-hanson	\N	0.7	fuzzy
2816	Steve Steve Hanson	\N	\N	steve-hanson	\N	0.7	fuzzy
2817	Steven Sinofsky	\N	Steven Sinofsky	steven-sinofsky	\N	0.9	exact
2818	Steven Sinofsky Brad is really at 10. being gracious and above reproach in this negotiation will go a long way to stopping steve from trashing you. you are right about the pr and i am very sensitve to it. I will handle it moving foward with jay, you can always blame jay, we will tell brad that you have removed yourself. I will charge you a one million dollar fee ( i will not get insulted if you choose not to ). Right at the end, not for jay , I will attempt to specifillay get samsung approved. letting steve feel good that he fucked you already , will minimize the moving forward , so i do not want to give up the higher amount demadn until the very last minute On Wed, Apr 3, 2013 at 9:59 AM, Steven Sinofsky	\N	Steven Sinofsky	steven-sinofsky	\N	0.7	fuzzy
2819	Steven Sinofsky It does talk about what you were doing when you were there though you didn't use the name On Monday, May 13, 2013, Steven Sinofsky wrote: Ok. He just doesn't like the topics. No mention of Microsoft or anything. Just related to the On May 13, 2013, at 8:43 PM, "Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2820	Stewart Oldfield	\N	\N	stewart-oldfield	\N	0.9	exact
2821	Stewart Oldfield	stewart.oldfield@db.com	\N	stewart-oldfield	\N	0.9	exact
2822	Stewart Oldfield	bradley.gillin@db.com	\N	stewart-oldfield	\N	0.9	exact
2823	Stewart Oldfield	joshua.shoshan@db.com	\N	stewart-oldfield	\N	0.9	exact
2824	Stuart Hameroff	\N	Stuart Hameroff	stuart-hameroff	\N	0.9	exact
2825	Stuart R - (hameroff) Hameroff	\N	Stuart Hameroff	stuart-hameroff	\N	0.7	fuzzy
2826	Stuart R- (hameroff) Hameroff	\N	Stuart Hameroff	stuart-hameroff	\N	0.7	fuzzy
2827	Su	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2828	Sub ect: • e: 130? On Thu, Aug 22, 2013 at 9:09 AM, David Mitchell Can I come over at noon or 1 Please note new location: DAVID MITCHELL Mitchell Holdings 801 Madison Avenue New York NY 10065 wrote: On Aug 22, 2013, at 8:50 AM, "Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2829	Subje : e: number? On Wed, Sep 15, 2010 at 9:45 PM Call me Sent from my BlackBerry® wireless device wrote: Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2830	Sultan Ahmed Bin Sulayem	\N	Sultan Ahmed bin Sulayem	sultan-ahmed-bin-sulayem	\N	0.9	exact
2831	Susan Hamblin	susan.hamblin@gmail.com	Susan Hamblin	susan-hamblin	\N	0.9	exact
2832	TOMMY MOTTOLA	\N	Tommy Mottola	tommy-mottola	\N	0.9	exact
2833	Tancredi Marchiolo	\N	Tancredi Marchiolo	tancredi-marchiolo	\N	0.9	exact
2834	Tazia Smith	\N	\N	tazia-smith	\N	0.9	exact
2835	Tazia Smith/db/dbcom To: "'effrey e stein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2836	Tazia Smith/db/dbcom To: "jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2837	Tazia Smith/db/dbcom To: "jeffrey epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2838	Terje Roed-Larsen	\N	Terje Roed-Larsen	terje-roed-larsen	\N	0.9	exact
2839	Thomas Turrin	\N	\N	thomas-turrin	\N	0.9	exact
2840	Thomas Turrin Tom is preparing gift tax returns for LDB and DRB.=C2 I have no visibility on gift tax return other than tax calculation.=C2 Torn has all info from Melanie and all info on 2013 GRAT's, =u> On Sep 23, 2014, at 8:41 AM, "Jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2841	Thomas Turrin c » Tom is preparing gift tax returns for LDB and DRB.=C2 I have no visibility on gift tax return other than tax calculation.=C2 Torn has all info from Melanie and all info on 2013 GRAT's, =u> On Sep 23, 2014, at 8:41 AM, "Jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2842	Tim Zagat	\N	Tim Zagat	tim-zagat	\N	0.9	exact
2843	Tim Zagat	tim@zagat.com	Tim Zagat	tim-zagat	\N	0.9	exact
2844	Tom Pritzker	\N	Tom Pritzker	tom-pritzker	\N	0.9	exact
2845	Tom Pritzker	tpritzker@pritzkerorg.com	Tom Pritzker	tom-pritzker	\N	0.9	exact
2846	Tom Pritzker	tpritzker@pritzkerorg.co	Tom Pritzker	tom-pritzker	\N	0.9	exact
2847	Tommy Mottola	\N	Tommy Mottola	tommy-mottola	\N	0.9	exact
2848	Trip Itinerary Your Confirmation number is: 144870 Phone#: Passenger Name: i Date & Time: Monday, May 18, 2015 1:43 PM Car Type: Camry WiFi / Similar '• Passengers/Luggag 1 passenger(s) / 2 pieces of luggage e	lesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	1	email
2849	Tyler Shears cs ' 'effrey =pstein	jeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2850	Tyler Shears jeffrey epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2851	Una Pascal	\N	Una Pascal	una-pascal	\N	0.9	exact
2852	Una Pascal	upascalftcvi@gmail.com	Una Pascal	una-pascal	\N	0.9	exact
2853	Vahe Stepanian	\N	\N	vahe-stepanian	\N	0.9	exact
2854	Valdson Cotrin	\N	Valdson Cotrin	valdson-cotrin	\N	0.9	exact
2855	Valeria Chomsky	\N	\N	valeria-chomsky	\N	0.9	exact
2856	Valeria Chomsky	valeria.chomsky@gmail.com	\N	valeria-chomsky	\N	0.9	exact
2857	Valeria Chomsky Forwarded message HI Valeria... just checking in..might you know if you will stay over or will need to fly home the evening of May 20? On May 14, 2015, at 9:01 AM, Valeria Chomsky	\N	\N	valeria-chomsky	\N	0.7	fuzzy
2858	Valeria Chomsky Unfortunately Jeffrey will not be staying over. Would after Work on June 2 be an option? 5pm? 6pm? Sent from my iPhone On May 27, 2015, at 5:34 PM, Valeria Chomsky	\N	\N	valeria-chomsky	\N	0.7	fuzzy
2859	Valeria Chomsky awful wrote: On Wed, Jan 17, 2018 at 6:38 PM, Valeria Chomsky	\N	\N	valeria-chomsky	\N	0.7	fuzzy
2860	Valeria Chomsky yes, the money in trust for them originally came from Noam correct? On Sun, Jul 2, 2017 at 12:48 AM, Valeria Chomsky	\N	\N	valeria-chomsky	\N	0.7	fuzzy
2861	Valeria Chomsky your apt is at 301 East 66 . where in nj as i can send my car if you like On Thu, Oct 1, 2015 at 10:15 PM, Valeria Chomsky	\N	\N	valeria-chomsky	\N	0.7	fuzzy
2862	Valeria Chomsky your apt is at 301 East 66 . where in nj as i can send my car if you like On Thu, Oct I, 2015 at 10:15 PM, Valeria Chomsky	\N	\N	valeria-chomsky	\N	0.7	fuzzy
2863	W. Daniel Hillis	\N	Danny Hillis	danny-hillis	\N	0.9	exact
2864	Wallace Cunningham	\N	Wallace Cunningham	wallace-cunningham	\N	0.9	exact
2865	Warwick Wicksman	\N	\N	warwick-wicksman	\N	0.9	exact
2866	Warwick Wicksman	warwick_wicksman@gensler.com	\N	warwick-wicksman	\N	0.9	exact
2867	We will work it out Thanks On Nov 29, 2018, at 5:10 PM, .1  wrote: there are irrigati=n electric landscpae electric gsj electric, internet. st=reo , only mike, the barge can b= done by many PM L.51 GS <mailt wrot=: Good Afternoon	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2868	Woody Allen	\N	Woody Allen	woody-allen	\N	0.9	exact
2869	Wray epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2870	_I	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2871	ann rodriquez	\N	\N	ann-rodriquez	\N	0.9	exact
2872	antoine verglas	\N	Antoine Verglas	antoine-verglas	\N	0.9	exact
2873	arda beskardes	\N	Arda Beskardes	arda-beskardes	\N	0.9	exact
2874	bellaklein	\N	Bella Klein	bella-klein	\N	0.9	exact
2875	bellaklein	bklein575@gmail.com	Bella Klein	bella-klein	\N	0.9	exact
2876	brice Gordon	\N	Brice Gordon	brice-gordon	\N	0.9	exact
2877	brice gordon	\N	Brice Gordon	brice-gordon	\N	0.9	exact
2878	brice gordon	beordon.lsj@gmail.coml	Brice Gordon	brice-gordon	\N	0.9	exact
2879	brice gordon	bgordon.lsj@gmail.com	Brice Gordon	brice-gordon	\N	0.9	exact
2880	charset=ISO-8859-1 Content-Transfer-Encoding: quoted-printable great, please lets see each other On Sun, Feb 2, 2014 at 1:53 PM	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2881	come soon On Fri, Jul 16, 2010 at 10:33 AM, Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2882	daphne wallace	\N	Daphne Wallace	daphne-wallace	\N	0.9	exact
2883	did you find your new computer	ijeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2884	eevacation mail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2885	eevacation mail.com	evacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2886	effre E	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2887	effre E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2888	effre e stein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2889	effre e stein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2890	effrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2891	effrey E	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2892	ehud barak	\N	Ehud Barak	ehud-barak	\N	0.9	exact
2893	ehud barak	ion@gmail.com	Ehud Barak	ehud-barak	\N	0.9	exact
2894	emad hanna	\N	Emad Hanna	emad-hanna	\N	0.9	exact
2895	emad hanna	emad.hanna01@gmail.com	Emad Hanna	emad-hanna	\N	0.9	exact
2896	george church	\N	George Church	george-church	\N	0.9	exact
2897	george church	gc@harvard.prlit	George Church	george-church	\N	0.9	exact
2898	george church	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2899	get a price for islland roa=s or better roads to lay a 8 by 50 asphalt strip up the side of the hill	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2900	harry Beller	\N	Harry Beller	harry-beller	\N	0.9	exact
2901	ike Groff	\N	\N	ike-groff	\N	0.9	exact
2902	ike groff Groff	\N	\N	ike-groff	\N	0.7	fuzzy
2903	ion nicola	\N	\N	ion-nicola	\N	0.9	exact
2904	ion nicola	ionnicola@hotmail.com	\N	ion-nicola	\N	0.9	exact
2905	j=ffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2906	j=ffrey E	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2907	j=ffrey epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2908	je=frey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2909	jeevS®gmail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2910	jeevacatio=®gmail.com	jeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2911	jeevacation	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2912	jeevacationaumail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2913	jeevacation®gmail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2914	jef=rey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2915	jeff=ey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2916	jeffr=y E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2917	jeffrcy E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2918	jeffrcy cpstcin	jcevacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2919	jeffrcy cpstcin	jcevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2920	jeffre E	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2921	jeffre e stein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2922	jeffre= E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2923	jeffrey =	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2924	jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2925	jeffrey E	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2926	jeffrey E	jeevacation@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2927	jeffrey E	jeevacation@grnail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2928	jeffrey E	jeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2929	jeffrey E	jeevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2930	jeffrey E	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2931	jeffrey E	jeevacation@omail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2932	jeffrey E	leevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2933	jeffrey E	ieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2934	jeffrey E	jeevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2935	jeffrey E	jeevacation@smail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2936	jeffrey E	evacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2937	jeffrey E	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2938	jeffrey E. jeevacation=gmail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2939	jeffrey E."=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2940	jeffrey E."=20	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2941	jeffrey E.=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2942	jeffrey E=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2943	jeffrey E?	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2944	jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2945	jeffrey Epstein	\N	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2946	jeffrey Epstein	jeevacation@runail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2947	jeffrey Hello Joi ...Jeffrey plans to arrive the institute approximately Ilam on Sunday March would like to meet with you privately for a bit...would llam work for you? >>>>>>>>> >>>>>>>>> >>>>>>>>> >>>>>>>>> E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2948	jeffrey e stein	eevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2949	jeffrey epstein	\N	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2950	jeffrey epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2951	jeffrey epstein	mailtoleevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2952	jeffrey epstein	ieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2953	jeffrey epstein	jeevacation@gmail.coml	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2954	jeffrey epstein	jecvacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2955	jeffrey epstein	on@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2956	jeffrey epstein	jeevacation@gmail.comj	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2957	jeffrey epstein	jeevacation@gmail.corn	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2958	jeffrey epstein	mailtoieevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2959	jeffrey epstein	ieevacation@omail.caral	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2960	jeffrey epstein	mailtojeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	0.9	exact
2961	jeffrey epstein	jeevacation@qmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2962	jeffrey epstein=	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2963	jeffrey=E	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2964	jeffrey=E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2965	jeffreyepstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2966	jetfrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2967	le mail	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2968	le vacation	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2969	le=frey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2970	leevacation	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2971	leffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2972	lelfrey epsteirr	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2973	lesley Groff	\N	Lesley Groff	lesley-groff	\N	0.9	exact
2974	njef=rey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2975	njeffrey=E	vacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2976	no , but i will ask my conde nast friend On Fri, Nov 27, 2009 at 7:56 AM, Jeffrey Epstein	jeevacation@grnail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2977	no , but i will ask my conde nast friend On Fri, Nov 27, 2009 at 7:56 AM, Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2978	no , but i will ask my conde vast friend On Fri, Nov 27, 2009 at 7:56 AM, Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2979	ok=br> On Wed,=Jan 10, 2018 at 1:03 PM, Lesley Groff	lesley.jee@gmail.com	Lesley Groff	lesley-groff	\N	1	email
2980	paul krassner	\N	Paul Krassner	paul-krassner	\N	0.9	exact
2981	qb>"jeffrey =	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2982	qb>"jeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2983	reevacation© mail.com	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2984	reffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2985	rich=rdkahnl2	richardkahn12@gmail.com	Richard Kahn	richard-kahn	\N	1	email
2986	rjeffrey E	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2987	sorry the last email was not complete.. i asked jean luc if he would take the girl with him on a private plane this week, he asked who it was , i told him to meet her.. that s it„ nothing to do with modeling sorry for the confusion On Mon, Oct 26, 2009 at 4:51 PM, Jeffrey Epstein	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
2988	svetlana	\N	Svetlana	svetlana	\N	0.9	exact
2989	tony	\N	Tony	tony	\N	0.9	exact
2990	valdson cotrin	\N	Valdson Cotrin	valdson-cotrin	\N	0.9	exact
2991	• Richard Joslin	jeevacation@gmail.com	Jeffrey Epstein	jeffrey-epstein	\N	1	email
\.


--
-- Name: communication_pairs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.communication_pairs_id_seq', 1, false);


--
-- Name: edge_sources_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.edge_sources_id_seq', 1, false);


--
-- Name: entities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.entities_id_seq', 1, false);


--
-- Name: relationships_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.relationships_id_seq', 1, false);


--
-- Name: resolved_identities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.resolved_identities_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict yQ0uosZjIwsK7EKQ5uzLgBWLBSbLuzWaymyt36Ju2t3begYaZLvwggHPbQVq0vk

