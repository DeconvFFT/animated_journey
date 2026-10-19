# Hindu visual language: art traditions, temple architecture and iconography for an animated life film — research notes

*Sonnet researcher, track `hindu-visual`, Monday 2026-10-19 (week 1 of 19; premiere Saturday 2027-02-27). Read first: `CHARTER.md`, `DECISIONS.md` (D-16, D-27, D-28, D-29; W-23, W-32 to W-34, W-38, W-40, W-46; O-36 to O-45 as proposed in `reviews/04-hindu-mobile-briefs-review.md`), the cinematic-quality, animated, ai-imagery, theatrical-delivery, agent-pipeline and craft-visual playbooks. Nothing in `CHARTER.md`, `DECISIONS.md`, `ROADMAP.md`, `PLAN-ON-A-PAGE.md`, `CLAUDE.md` or `.claude/` was edited; no code was written for the film and nothing was committed.*

**How to read the labels.** (S) sourced, with the source number in brackets. (M) measured in this sprint, on a synthetic chart, in the cloud container (fixture in `research/hindu-visual-fixtures/`). (J) the researcher's judgment, to be tested. UNVERIFIED means a fact I could not confirm from a page I actually read; each carries what would confirm it. Every fast-moving fact carries the date it was read (2026-10-19 unless stated). A source marked "digest only" is a URL I saw in a search result whose page I could not open (blocked, rate-limited, or not tried); I never quote its wording as if I had read it. Nothing here is legal advice: every legal line is a question for the T10 consult and names its jurisdiction. The repo is public: no names, places or family details appear; the households in the worked examples are invented.

**Three things the brief assumed that the sources did not support** (so the maker is not surprised later):

1. "The UK treats photographs of public-domain 2D art differently since 2023." I found no 2023 change. What exists is Intellectual Property Office guidance, "Updated 4 January 2021", saying a faithful digitised copy "seems unlikely" to be original and admitting "a degree of uncertainty" [24]. A UK High Court case, Antiquesportfolio.com v Rodney Fitch (2000), appeared in a search digest with no outcome stated, so I do not rely on it.
2. "Buying the painting does not transfer copyright in India." True for a painting that already exists. For a painting commissioned for payment, s.17(b) of the Copyright Act makes the person who commissioned it the first owner "in the absence of any agreement to the contrary" [25][26], but its proviso says that for a work incorporated in a cinematograph film that default does not affect the author's rights [25]. Either way the written, signed licence or assignment under s.19 is the control, so the practical rule in the brief survives; the reasoning is different (F9).
3. "Extra and missing arms, swapped attributes and garbled ornaments are the documented AI failure modes." I found no measurement of arm counts. The documented failures are cultural: a "very white" Rama, sexualised goddesses, an always-angry Hanuman, tantra rendered as satanic, a saint mistaken for Rama, a "too feminine" Ram [81][82]. Arm-count and attribute errors stay UNVERIFIED (expected, not measured) and are treated as likely in the rules.

---

## Summary

1. **Gate, then rank.** Fourteen candidate traditions plus the floor arts were checked against D-28. Nine pass unflagged on subject and origin (Pattachitra, Kerala murals, Tanjore and Mysore, Srikalahasti Kalamkari, Phad, Cheriyal, Kalighat for its deity plates, Madhubani) and the floor arts and shadow-puppet arts pass with a note. Pahari/Kangra and Rajput court painting are flagged (Mughal-trained painters at Guler; Bundi and Kota "influenced directly by Mughal painting") [35][37]; Machilipatnam Kalamkari is out ("Persian-influenced motifs") while Srikalahasti stays [41]; Togalu puppets carry an "Islamic culture" costume flag [44]. A tradition is eligible only if it is hers (O-36, O-37, O-40); the scored matrix ranks the eligible ones (section "Templates and deliverables", T1).
2. **The phone floor is 4 px, not 2 px (M).** On a synthetic chart with grain, a 1080p H.264 CRF 18 phone master keeps a 1 px black line at 0.98 of full contrast, so the master is not the problem. After a WhatsApp-class recompression (two proxies: 1280x720 at 2.5 Mb/s and 640x360 at 0.5 Mb/s, both UNVERIFIED stand-ins) a black line placed at a half-pixel keeps 0.86 / 0.48 at 2 px, 0.95 / 0.61 at 3 px and 1.07 / 0.83 at 4 px. Hatching at 1 px with 3 px pitch drops to 0.48 / 0.00; 2 px dots to 0.56 / 0.20; 2 px pierced holes to 0.63 / 0.26. Floor: 4 px for any line that carries meaning, 3 px for decoration that may be lost, dots 6 px, holes 4 px, hatch stroke 3 px at 9 px pitch, no 1 px anything. Cinematic-quality T2 decision 3 (2 px) and T1 PR2 need a phone delta.
3. **Which traditions hold on a phone (M and J).** Hold: Kalighat's bold brush, Kerala five-colour blocks, shadow-puppet silhouettes (not their perforations), cream-on-dark floor lines at 3 px or more. Lose their line: Madhubani hatching and double-line fill, Srikalahasti pen detail, Pahari fine modelling and flowers, Tanjore relief and glass-bead glints, Pattachitra's fine border pattern. Madhubani and Pattachitra survive only if redrawn coarser, and then look like a different hand.
4. **Animation to a standard is rare for these traditions.** Verified exemplars are few: *Ramayana: The Legend of Prince Rama* (dated 1992 in the brief and 1993 on Wikipedia; Indian premiere 10 Jan 1993; 4K re-release in India 24 Jan 2025) [91]; *Sita Sings the Blues* (2008; Rajput-like painted scenes, shadow-puppet narrators, vector musical numbers) [92]; Nina Sabnani's craft films, including *Hum Chitra Banate Hain* (2016, Rajat Kamal 2017) [100]; *Bombay Rose* (2019, hand-painted, about six years) as a digest-only fact [101]; devotional features *Mahavatar Narsimha* (25 Jul 2025; 3D) and *The Legend of Hanuman* (2021 to 2025) [94][95]. I found no verified standard-level animated film for Madhubani, Kalighat, Kerala murals, Tanjore, Cheriyal or Phad, so each is a prototype risk and the first fixture must be a traced plate, not a promise.
5. **The strongest fits for a life film are structural, not stylistic (J).** The floor arts are native line-draw and are what her hands may have made (W-38: decisions 2 and 11 become one thing). The Phad and Cheriyal scroll is a life told in panels by a storyteller (a camera that pans, a pointer, a lamp). The shadow puppet has four to twelve hinge joints [44], which is `data-pivot` in the existing Route A SVG rules [craft-visual].
6. **Architecture is one table once the region is known.** Nagara (curvilinear shikhara, amalaka, kalasha), Dravida (stepped vimana, tall gopuram, mandapa halls, tank), Vesara (a Chalukya-Hoysala hybrid) [52][53][54][55]. Kalinga (Odisha), Bengal and Kerala temples sit outside the trio (J). Clean open images: CC0 for a Nagara shikhara (Kandariya Mahadeva) [21], CC0 for a makara relief [22], a public-domain 1809 aquatint of the Thanjavur vimana [23], and public-domain 1858 gopuram photographs at the Met [5]. Most other Commons photographs are CC BY-SA, which is a share-alike duty if traced.
7. **Four architectural elements are shared and stay out by default.** Jaali (pre-Islamic temple screens persisted, but the geometric and calligraphic development is Indo-Islamic) [58], chhatri (Rajasthani origin, but "found particularly within Mughal architecture"; Hindu cenotaphs exist) [57], cusped arch (Gujarat's Chaulukya toranas were temple gateways and are, from background knowledge, scalloped, so the arch alone proves nothing; the torana page does not say) [56], dome (an onion dome is Persianate, (J); the amalaka disc and kalasha urn that crown a Nagara tower are not domes) [53]. Each entry carries a one-line origin note and a question to the maker.
8. **Iconography is form-first, and the texts disagree with each other.** Gopinatha Rao (1914, public domain) records agamic descriptions that differ among themselves: Saraswati with a rosary and book, or with a veena; Lakshmi with two hands beside Vishnu and four alone; Sita to Rama's left in a 16th to 17th century bronze group while another source puts her on the right; the 24 forms of Vishnu differ only by which of four attributes sits in which hand [61][62][63][78]. So every shot brief names the form and copies her home image where one exists (O-38); the checklist supplies defaults and "ask" flags. Mirroring an asset changes handedness, so "flip horizontally" is a banned operation on deity assets.
9. **Respect rules can be written as shot rules.** Twenty are in section "Templates and deliverables", T4, each with a test and its source: nothing on a surface that is stepped on or discarded and no footwear [80], no human held hand-in-hand with a deity (a South African Hindu priests' council called AI images of that "offensive") [85], no fabricated ritual (the Jagannath administration's police complaint over AI video of milk poured by crane, January 2026) [83][84], no cartoon casualness (the VHP objected to gods "drawn as cartoon figures" in 1983 to 1992; *Adipurush* 2022 to 2023 is the anti-exemplar) [91][93].
10. **No generated deity figure in the public cut.** The Hindu American Foundation (6 Oct 2025, updated 24 Oct 2025) says "AI images are not inherently sacred" and that correctness matters "independent of sincerity of devotional intent" [79]. Temple bodies that have acted: the Jagannath temple administration (complaint at Singhadwar police station, 20 to 21 Jan 2026) [83][84]. Tamil Nadu's HR&CE kept its ban on photography and video in temples when it eased phone rules (11 Oct 2026) [86]. I found no Tirumala or Nathdwara notice on AI images (UNVERIFIED). The safe route is symbols first, then hand-traced public-domain plates with the source logged, then the maker's own photograph of her shelf, then a commissioned painting with a written licence.
11. **Rights: a museum's licence is per record.** CC0 images: Cleveland (since January 2019) [1], Smithsonian (record-level CC0 on National Museum of Asian Art objects) [7][8], Met (CC0 icon on public-domain works; data CC0) [4][6 digest only]. Unrestricted public-domain downloads with a credit request: LACMA [10]. CC0 or public domain with exceptions: Rijksmuseum [11]. Public-domain images "generally": Philadelphia [13]. Personal and non-commercial only: Harvard [12]; V&A non-commercial [16]; British Museum CC BY-NC-SA (digest only) [17]. Wellcome varies by work: of 184 Kalighat catalogue results, 96 digitised items carry the Public Domain Mark, 3 are CC BY-NC (the Lakshmi plate among them) and 4 CC BY [14][15]. No terms found for the San Diego Binney collection [18]. Google Arts & Culture is view-only in practice [19 digest only].
12. **Commissioning is feasible and the paper matters more than the paint.** Marketplace listings seen in search digests (pages blocked, UNVERIFIED): a 12 by 18 inch Pattachitra at INR 15,000 with one to two weeks quoted; a 24 by 40 inch Pattachitra at INR 26,000; a 15 by 12 inch Tanjore with 22k gold at INR 21,600; Madhubani sets from about INR 4,200 [106][107]. Plan six to ten weeks end to end for a custom piece (J). The assignment must be written and signed (s.19), name the film use, the territory (worldwide, because the premiere country is unknown) and the term, because the defaults are India only and five years [25]. A GI registration protects the name on goods against misleading origin claims; it does not own a style [27].
13. **What agents can build as seekable SVG (Route A):** kolam and rangoli as parametric line-draw (`pathLength` and `stroke-dashoffset`), torana, kalasha, lotus, diya, Om and conch as vector, shadow-puppet cut-outs as layered SVG with `data-pivot` hinges. What needs a human hand (the maker in VectorCraft, or paper): any deity figure, Kalighat and Pattachitra faces, Tanjore gilding relief, Madhubani figure fields, the maker's proxy approval of every deity drawing.
14. **The `hindu_idiom` block (decision 11)** is written in "Templates and deliverables", T6, with two invented households filled in to show the block yields two different films. It never touches decisions 1 to 10 except by reference; where she made kolam, alpana, embroidery or garlands, decision 2, decision 6 and decision 11 are one thing.
15. **Eight questions for the maker are keyed on the unknowns** (region, sampradaya, shelf, hands, deities on screen, the room, phone orientation, commissioning a name-free brief). The default until they are answered is "symbols only, landscape-first, no figure" (J).

---

## Findings by question

### F1. The traditions: region, sampradaya, subject, conventions, and what breaks in motion

Source for each row is in brackets; the last two columns are mostly (J) built on the sourced conventions. "Flag" is the D-28 status: **OK** (Hindu in subject and origin), **OK-note** (Hindu with a stated caution), **FLAG** (shared or ambiguous; out by default), **OUT**.

| Tradition | Region | Sampradaya and devotional setting | Hindu subject matter | Line, palette, figure conventions | What breaks when it moves | Flag |
|---|---|---|---|---|---|---|
| Pahari / Kangra | Kangra, Guler, Basohli, Chamba, Mandi (Himachal and neighbours) [35] | Vaishnava: Krishna lila, Gita Govinda, Bhagavata Purana; Sansar Chand "a devotee of Krishna" [35] | Radha and Krishna, Nala and Damayanti, Baramasa [35] | "Precise and fluid, lyrical, and naturalistic"; faces "finely modelled and shaded, giving them a porcelain-like delicacy"; cool fresh mineral colours; lush multi-green landscapes [35] | Modelled faces and soft landscape shading go flat in cut-outs; the fine flowers and hairlines are exactly what fails on a phone (M) | **FLAG**: began when "a family of Kashmiri painters trained in the Mughal painting style" sheltered at Guler [35]; a Cleveland Sansar Chand painting (2018.120) carries Takri and Persian inscriptions (digest of the Cleveland API record, UNVERIFIED). Basohli ("blazing colours bold lines", Vaishnava) is the earlier, bolder idiom [36] and is the only one worth proposing if the maker wants Pahari |
| Rajput Hindu court (Mewar, Bundi, Kota, Marwar, Kishangarh) | Rajasthan and Malwa [37] | Vaishnava manuscripts, Ragamala as bhakti [37] | Krishna from the Bhagavata, Ramayana, Ragamala; court and hunt scenes [37] | Mewar "the most traditionalist"; the pre-Mughal Chaurapanchasika group is "pre-Mughal Hindu painting"; Bundi "refined line and controlled palette" [37] | Court portraits and hunts are secular; devotional Mewar manuscripts are the usable subset | **FLAG**: Bundi and Kota "influenced directly by Mughal painting"; eastern Marwar "more open to Mughal influence" [37]. Sita Sings the Blues borrows the Rajput look [92] |
| Tanjore (Thanjavur) | Thanjavur, Tamil Nadu [33] | Vaishnava and Shaiva household icons; Krishna, Lakshmi, Rama are typical [33][51 digest] | Gods, goddesses and saints from the Puranas [33] | Central figure largest, under an arch or prabhavali; "rounded" faces, almond eyes; flat bright colours; gesso in high relief under gold foil, glass beads [33] | The gold relief and gems are lit surfaces: flat vector reads dead and a camera move needs a baked highlight pass; VectorCraft drops filters, so no filter-made glint [craft-visual]. Fine glints vanish on a phone (M) | **OK-note**: "angel-like seraphs often flank the main figure" [33]: winged attendants are flagged and omitted. GI 2007 to 2008 [33] |
| Mysore | Mysore, Karnataka [34] | Hindu gods and mythology; Wodeyar patronage [34] | Gods, goddesses, mythology [34] | "Delicate lines, intricate brush strokes, graceful delineation"; gesso "low in relief" compared with Tanjore [34] | As Tanjore, with finer line, so worse on a phone | OK |
| Kerala temple murals | Ettumanoor, Vadakkumnatha, Padmanabhapuram, Mattancherry [32] | Shaiva, Vaishnava, Devi temples; iconography follows dhyana slokas [32] | Ramayana, Shiva, Gajendra moksha [32] | Five colours (panchavarna): red, yellow, green, black, white; figures coloured by guna (sattvic green, rajasic red to gold, tamasic white or black) [32] | The guna colour is meaning, so it must not be recoloured to an era palette (J); wall-plaster texture is the ground | **OK-note**: the Mattancherry site is a palace, and the sites list also names "several churches" [32]; use the style, not the set |
| Pattachitra (Odisha; Bengal patachitra is a separate GI) | Puri, Raghurajpur, Parlakhemundi, Sonepur [30][49] | Jagannath cult; Vaishnava [30] | Jagannath, Radha-Krishna, ten avataras from the Gita Govinda, Ramayana, Mahabharata [30] | "Bold and clean and angular and sharp" lines; no landscape or perspective; fixed postures; a decorative border on every painting; red ground; five natural colours; drawn directly with the brush, no pencil [30]; each scene set within a border, with "frontal perspective" [49] | The border is the frame and must stay still; parallax breaks the no-perspective rule; the fine floral border and faces fail on a phone unless redrawn at 4 px or more (M) | OK. GI Odisha 10 Jul 2008; Bengal Patachitra 28 Mar 2018 [30] |
| Madhubani (Mithila) | Madhubani district, Bihar, and Nepal [31] | Mithila: Rama and Sita's wedding, Shiva-Parvati and the Mahavidyas; kohbar painted in the wedding chamber [31] | Deities, epics, tulsi, weddings, courts [31] | "No space is left empty"; two-dimensional; natural pigments; five styles (Bharni, Kachni, Tantrik, Godna, Kohbar) [31] | Horror vacui shimmers with any scale change; hatching and fill dots vanish after recompression (M) | OK: the art "transcend[s] caste distinctions" [31] and marketplace listings name artists of different communities (digest); the exclusion rule governs motifs, not artists (open question V6). GI status reported, year not read from a registry [31][51 digest] |
| Kalamkari, Srikalahasti | Srikalahasti, Andhra Pradesh [41] | Temple scrolls, hangings, chariot banners [41] | Brahma, Saraswati, Ganesh, Durga, Shiva, Parvati; Ramayana, Mahabharata, Puranas [41] | "Entirely hand worked" with a kalam (pen), freehand outline then fill [41] | Pen line is the identity and falls below 3 px (M) | **OK**; the Machilipatnam sibling is **OUT** ("Persian-influenced motifs"; Golconda and Mughal patronage) [41]. GI Srikalahasti April 2005 and Machilipatnam April 2008 [41]; other sources give 2006 and 2009 [51 digest] |
| Phad | Rajasthan; Bhilwara [40] | Folk deities Pabuji and Devnarayan; Joshi painters, Bhopa priest-singers, Rebari worshippers [40] | Narratives of folk deities; modern versions of Ramcharitmanas and Gita [40] | A long cloth, about 15 ft (Pabuji) or 30 ft (Devnarayan); "vegetable colors" [40] | The figures do not move; the Bhopa does. Camera as the pointer along the scroll is native (J) | OK-note: "traditionally practiced exclusively by the Joshi community" [40], so commission or credit rather than imitate |
| Cheriyal | Telangana [39] | Nakashi painters and Kaki Padagollu storytellers [39] | Krishna Leela, Ramayana, Mahabharata, Shiva Puranam, Markandeya Puranam; folk ballads of Gauda and Madiga communities [39] | Vertical scroll of horizontal panels with floral borders, up to 40 to 45 ft; "vivid hues, mostly primary colors, with a predominance of red in the background" [39] | Dense crowds per panel fail on a phone; panel-by-panel reveal is native | OK. GI 2008 [39] |
| Kalighat | Calcutta, near the Kalighat Kali temple [29] | Shakta (Kali most drawn) [29] | Kali, Shiva, Parvati, Durga, Lakshmi, Saraswati, Ganesha, Krishna, Radha, epics [29] | "One long bold sweep of the brush"; bold outlines, minimal background; shading as a wash darker at the edges [29] | The wash is baked into each figure; limbs as hinged cut-outs hold (M: bold lines survive) | **OK-note**: also satirical babu and bibi, courtesans and news events [29]; and some public-domain plates are comic or irreverent (section F8) |
| Nathdwara pichwai | Nathdwara, Rajasthan [38] | Pushtimarg (Vallabhacharya); Shrinathji; made for the temple on the chief priest's commission [38] | Seasonal and festival scenes: Govardhan Puja, Sharad Purnima, Raslila, Holi, Annakut, Gopashtami; gopis and cows [38] | Cotton, opaque watercolour, gold and silver leaf [38] | A pichwai hangs behind an image of Shrinathji; shown without him it changes meaning (J) | **OK-note**: sampradaya-specific; wrong in a Shaiva or Smarta home. Mughal influence not stated in the source read; whether the workshop idiom has Rajput-Mughal court roots is UNVERIFIED |
| Raja Ravi Varma | Travancore; press at Ghatkopar then Malavli [48] | Pan-Hindu popular devotion | Gods and goddesses from the Mahabharata, Ramayana and Puranas as oleographs [48] | European academic technique, goddesses modelled on South Indian women [48] | Naturalistic oil modelling goes uncanny if animated; use as stills with respect rules | **OK-note**: the colonial-Christian layer in some prints (cherubs, disc halos, candles, church bells) is the brief's lead and is UNVERIFIED: nothing I read confirmed it; check each plate |
| Shadow puppets: Tholu Bommalata (Andhra), Togalu Gombeyaata (Karnataka) | Andhra, Telangana, Karnataka [42][43][44] | Epic performance, all night, invocation first (to Ganesha in Karnataka) [42][43] | Ramayana, Mahabharata, Puranas, folktales; Hanuman the central hero [42][43][44] | Translucent hide (antelope for gods and heroes, deer, goat); Andhra puppets up to 3 ft wide and 6 ft high, profile figures with wide circular eyes, "several geometric perforations" for garlands and jewellery; four to twelve joints [42][44] | Perforations are pierced holes: below 4 px they close (M). Backlit colour glow is the look: a translucent layer, not a fill | OK. **FLAG** for Togalu: "blend influences from the Halebid Hoysaleshwara temple and Islamic culture", men with "long thin moustaches, long beards and boots" [44] |
| Floor arts | Kolam (Tamil Nadu), muggu (Andhra, Telangana), rangoli (Karnataka, Maharashtra), alpana (Bengal), mandana (Rajasthan, Malwa), aipan (Uttarakhand), jhoti or chita (Odisha), pookalam (Kerala), sathiyo (Gujarat) [46] | Household: welcoming Lakshmi, thresholds, Margazhi and Andal in Sri Vaishnavism [45][46] | Lotus, mango, vase, fish, birds, diya, Ganesha, Lakshmi [46]; alpana: owl, granary, conch, lotus, rice sheaf [47] | Rice flour (South) or gypsum (North); pulli dot grid and a closed stroke around each dot (sikku) [45]; alpana freehand with fingertips, "without the use of stencils or patterns" [47] | Nothing breaks: it is drawn, then swept or walked away [45]. Thin lines and tiny dots do (M) | OK; swastika forms need the maker's call (T9 below) |

### F2. What has been animated, by whom, and with what motion vocabulary

| Title or maker | Year | Who | Look and motion | What I verified | Verdict for us |
|---|---|---|---|---|---|
| *Ramayana: The Legend of Prince Rama* | 1992 (brief) or 1993 (Wikipedia); Indian premiere 10 Jan 1993 | Yugo Sako, Koichi Sasaki, Ram Mohan; Nippon Ramayana Films; animation Doga Kobo; about 450 artists from 1990 [91] | Japanese cel animation; "an Indian version of the Disney style, with big dewey eyes" (festival director Alan Franey) [91] | Indian advisers on customs; the VHP objected to gods "drawn as cartoon figures"; the Indian government "later declined" collaboration; 4K remaster re-released in India 24 Jan 2025 [91] | Craft benchmark and a precedent that animated gods are themselves contested for some devotees (O-42). Reviewer: Sita "looks like Snow White in a saffron sari" (India Today) [91] |
| *Sita Sings the Blues* | 2008 (Berlin, 11 Feb) | Nina Paley [92] | Four registers: painted figures like 18th-century Rajput painting; three silhouette shadow-puppet narrators (Chhaya Natak); vector musical numbers; Squigglevision [92] | Free download March 2009 under CC BY-SA, changed to CC0 in 2013; the 1920s Annette Hanshaw recordings were never truly free (US$50,000 negotiated); April 2009 Hindu Janajagruti Samiti petition called it "derogatory"; Paley later said Rama "is not depicted well" [92] | Style reference only: no assets, no tracing. Lesson: separate registers (picture, narrator, song) by medium |
| Nina Sabnani films | 2005 to 2016 | Industrial Design Centre, IIT Bombay; *Hum Chitra Banate Hain* ("We Make Images", 2016, Rajat Kamal 2017) with a Bhil artist; *Baat Wahi Hai* (2011); *Tanko Bole Chhe* (2009, "The Stitches Speak"); *Mukund and Riaz* (2005) [100] | Animation built from practising artists' craft; cloth and stitch kept tactile (digest only) [100][101] | Filmography and awards [100]; collaboration with Gujarat embroiderers and folk fablers from digest only | Method model: work with a practising hand, credit them, keep the craft's texture. D-28 flags: Bhil art is Adivasi (ask); *Mukund and Riaz* is, from background knowledge and not confirmed here, a story of two friends divided by Partition with a Muslim character (method only) |
| *Bombay Rose* | 2019 | Gitanjali Rao; opened Venice Critics' Week | Hand-painted frame by frame, about six years [101] | Digest only (Cartoon Brew, Screen Daily, AWN) | Proof that painterly looks cost years; we get 19 weeks |
| Studio Eeksaurus | Founded 2009, Mumbai | Suresh and Nilima Eriyat [102] | Ad films, clay and hand-drawn shorts; *Kandittund!* (2021) won Best Animation Film at the 69th National Awards [102] | Digest only; nothing found on Hindu or folk-art films | Not a Hindu-visual exemplar; kept as an Indian independent-craft reference |
| *Arjun: The Warrior Prince* | 25 May 2012 | UTV and Disney; Tata Elxsi animation; director Arnab Chaudhuri; about 300 people; action workshopped with Kalaripayattu and Thang-Ta performers [96] | 2D action | Box office INR 24.4 million against INR 75 million; LA Times: "stiff and presentational, resembling a rushed rotoscoping job"; NY Post: computer-game-style [96] | Anti-exemplar: game-like stiffness |
| *The Legend of Hanuman* | 29 Jan 2021 to 11 Apr 2025, six seasons, 52 episodes | Graphic India; Sharad Devarajan, Jeevan J. Kang, Charuvi Agrawal; Disney+ Hotstar [95] | "Comic book-inspired animation" (a cited title); animatics so actors could perform [95] | Dates and credits [95]; no reception section | Big-studio benchmark, not our scale |
| *Mahavatar Narsimha* | Premiere 25 Nov 2024 (IFFI); release 25 Jul 2025 | Director Ashwin Kumar; Kleem Productions, presented by Hombale Films; 131 minutes [94] | 3D, photorealistic; sources named: Vishnu, Varaha, Narasimha and Padma Puranas; visits to Ahobila and Hampi [94] | Highest-grossing Indian animated film, INR 300 to 325 crore worldwide (estimates differ); critics praised the animation and called the violence excessive for children [94] | Benchmark for devotional respect and scriptural fidelity, not for style. Whether scholars were consulted: UNVERIFIED (one low-quality site claims 14) [103] |
| Amar Chitra Katha | 1967 on | Anant Pai; illustrators Ram Waeerkar, Dilip Kadam, Pratap Mullick and others; owned by Amar Chitra Katha Pvt Ltd [97] | Printed comics; the canonical popular look | Fire on 1 Oct 2025 destroyed original hand-drawn positives for about 200 early titles [97]; critics (Pritchett, 1995) call its history selection "invidiously selective" [97] | Copyrighted: never trace a panel. A lineage the audience may feel, not a source |
| *Little Krishna* | 11 May 2009 on Nickelodeon | Big Animation (Reliance), India Heritage Foundation, powered by ISKCON Bangalore; 13 episodes of about 22 minutes; INR 50 crore [99] | 3D | Five FICCI Frames Awards, an Asian Television Award for Best Animation 2009 [99] | Shows a devotional family series is acceptable to broad audiences |
| *Sanjay's Super Team* | 2015 (Annecy, June) | Pixar, Sanjay Patel; Academy Award nomination [98] | Statues of Vishnu, Durga and Hanuman come alive in a temple; a lamp is read as an upturned bell; built from the director's own childhood puja with his father [98] | Production history only; no Hindu-group reaction found in the page read | Personal framing is the lesson (hers first). Whether living statues satisfy our respect rules is a separate question: they would need the maker's explicit yes under R6 and R9 |
| *Adipurush* | 2022 teaser to 2023 | Om Raut [93] | Live action with VFX | Teaser of 2 Oct 2022 criticised; slang in the mouths of gods; Ravana's "leather jackets"; a FIR (18 Jun 2023) and a PIL; the Allahabad High Court criticised the portrayal; the writer apologised in 2026 [93] | Anti-exemplar for the casual, comic or slangy register |
| *Chhota Bheem* | 2008 on | Green Gold | Mass-market children's 3D | **Not researched in this sprint (UNVERIFIED)**; kept as the stated floor to stay above | |

### F3. How each tradition reads on a 6-inch phone (fixture-tested, M-H1)

**Geometry first (J, assumptions stated).** A 6.1-inch 20:9 phone with a 2400 by 1080 panel has about 431 pixels per inch, so a device pixel is about 0.059 mm. Held at 35 cm that is about 0.58 arcminutes per pixel. Played full screen sideways, a 1080p video maps about one video pixel to one device pixel, so a 2 px line subtends about 1.2 arcminutes: at the edge of 20/20 acuity (about 1 arcminute, a textbook figure) and worse for a viewer over 50 without reading glasses. For comparison, one pixel of a 10 m wide cinema screen seen from 15 m is about 1.2 arcminutes and from 25 m about 0.7. Played upright in a chat, the 16:9 picture is fitted to the screen width, which scales it to about 0.56 of a pixel per video pixel (1080-pixel-wide display), so 2 px becomes 1.1 device pixels and 4 px becomes 2.25. The 2 px floor in cinematic-quality was set for a TV or room; the phone is the harder screen.

**Fixture (M-H1, [104]).** One 1920x1080 chart (`research/hindu-visual-fixtures/phone_chart.svg`) with seven cell types, temporal grain added (strength 7 of 255), ProRes master, three encodes (P1: 1080p CRF 18, cap 8 Mb/s; WA-HD proxy: 1280x720 at 2.5 Mb/s; WA-STD proxy: 640x360 at 0.5 Mb/s), a static and a slow-pan clip, and two display scalings (landscape 1.0, portrait 0.5625). "Contrast retained" is 1.00 for full ink contrast. **The two WA proxies are not WhatsApp's encoder.** They come from anecdotal reports: files about 640 pixels wide at about 500 kb/s, some at 15 fps (an OBS forum thread, digest only) [105], and an "HD" option that means 720p (how-to articles, digest only) [105]. The mobile-delivery track must measure real output with ffprobe on the project phone. Worst case of static and pan is shown. Values slightly above 1.00 are resampling overshoot.

Landscape full screen (one video pixel is one device pixel):

| Feature (at 1080p) | P1 (1080p CRF 18) | WA-HD proxy | WA-STD proxy | Reads as |
|---|---|---|---|---|
| Black line, 1 px, pixel-aligned | 0.98 | 0.59 | 0.25 | gone in WA-STD |
| Black line, half-pixel position, 2 px | 0.99 | 0.86 | 0.48 | marginal in WA-STD |
| Black line, half-pixel position, 3 px | 1.01 | 0.95 | 0.61 | holds, barely |
| Black line, half-pixel position, 4 px | 1.00 | 1.07 | 0.83 | safe |
| Hatching 1 px, pitch 3 px | 1.05 | 0.48 | 0.00 | lost (Madhubani fill) |
| Hatching 2 px, pitch 6 px | 1.05 | 1.04 | 0.50 | marginal in WA-STD |
| Hatching 3 px, pitch 9 px | 1.06 | 1.14 | 0.89 | holds |
| Cream line on indigo, 2 px | 1.00 | 0.93 | 0.60 | marginal (kolam on dark floor) |
| Cream line on indigo, 3 px | 1.01 | 1.09 | 0.87 | holds |
| Black dot, 2 px / 3 px / 4 px / 6 px | 0.78 / 0.99 / 1.02 / 1.02 | 0.56 / 0.90 / 1.09 / 1.08 | 0.20 / 0.34 / 0.49 / 0.92 | pulli and fill dots need 6 px in WA-STD |
| Hole in a black silhouette, 2 / 3 / 4 / 6 px | 0.75 / 0.99 / 0.98 / 1.03 | 0.63 / 0.86 / 1.03 / 1.11 | 0.26 / 0.38 / 0.78 / 1.11 | puppet perforations need 4 px |
| Black on red, 2 px / 4 px | 0.88 / 0.95 | 0.69 / 0.87 | 0.41 / 0.57 | outline on a red ground needs more than 4 px or a lighter fill |
| Red on yellow, 2 px / 4 px | 1.00 / 1.02 | 0.82 / 1.10 | 0.44 / 1.01 | holds at 4 px |
| Green on red, 2 px / 4 px | 0.86 / 0.96 | 0.62 / 1.02 | 0.29 / 0.66 | equal-brightness pairs fail |

Portrait inline (scale 0.5625): the clean P1 file itself drops to 0.34 to 0.46 at 1 px, 0.61 to 0.89 at 2 px, 0.90 to 1.08 at 3 px; through WA-STD a 3 px half-pixel black line keeps 0.61 and a 4 px line 0.85; a 4 px dot keeps 0.50 and a 6 px dot 0.91; a 4 px hole 0.67 and a 6 px hole 1.00.

**Reading it (J on top of M).** The threshold I use is "holds" at 0.6 and "safe" at 0.8 of full contrast. These are my criteria, not a standard. Findings: (1) the phone master is not where the loss happens; the chat recompression is, so the existing PR2 test (access-copy encode) cannot catch it; (2) 4 px is the floor for a meaning-bearing line, 3 px for decoration that may vanish; (3) dots 6 px, holes 4 px, hatch stroke 3 px at 9 px pitch; (4) coloured lines need luminance contrast, not just hue contrast; (5) design for landscape full screen and treat upright chat playback as a degraded view: at 0.56 scale even the clean file loses 2 px lines.

**Per tradition (what the fixture implies, J).** Native feature scale at the size a figure fills about a third of the frame height:

| Tradition | Identity feature | Needs at 1080p | As drawn on a phone | Redrawn at the floor |
|---|---|---|---|---|
| Kalighat | Bold brush outline, flat colour, wash | outlines 6 px or more, detail 4 px | Holds | Same drawing |
| Kerala murals | Thick outline, five flat colours | 4 to 6 px | Holds; ornament fades | Hold ornament at 4 px |
| Shadow puppets | Silhouette, perforation, backlit colour | holes 4 px or more | Silhouette holds; holes close | Enlarge and thin the perforations |
| Floor arts (kolam, alpana, rangoli) | Line and dot | cream on dark, line 3 to 4 px, dot 6 px | Holds if drawn this way; real grids are denser and fail | Fewer, larger pulli |
| Phad, Cheriyal | Large figures, red ground, black line, panels | line 4 px; no dense crowds | Phad holds; Cheriyal crowds fail | Cut panels to fewer figures |
| Pattachitra | Angular line, fine border pattern | outline 4 to 5 px; border motif 6 px or more | Figure holds; border blurs | Coarser border |
| Tanjore, Mysore | Gold relief, gems | outline 4 px; gem 6 px; gold as flat colour | Reads as flat gold | Bake the highlight, no filters |
| Madhubani | Hatching, double line, fill | hatch 3 px at 9 px pitch; dots 6 px | Hatch is mush | Coarse hatch changes the look |
| Kalamkari (pen) | Fine pen line | 3 px or more | Line lost | Heavier line |
| Pahari / Kangra | Modelling, hairline flowers | not achievable at phone scale | Lost | Different art |
| Pichwai | Dense lotus and cow repeat, gold leaf | repeat unit 6 px or more | Mush | Fewer, larger units |

### F4. Temple-architecture vocabulary for sets, frames and transitions

Orders (S): **Nagara**, the northern style with the curvilinear *shikhara* ("mountain peak") over the sanctum, topped in Odisha by an amalaka disc and kalasha urn "by at least 600 CE" [53]; **Dravida**, the southern style whose tiered pyramidal tower over the sanctum is the *vimana* and whose big entrance towers are *gopurams*, "the tallest and dominant element" from the 12th century on; later gopurams "overshadowed the inner vimana" [52][54]; **Vesara**, a hybrid that "originated in the region between the Krishna and Tungabhadra rivers", with roots in the Badami Chalukyas and continued by the Hoysalas, at Lakkundi, Dambal, Itagi and Gadag [52]. Regional types outside the trio (Kalinga in Odisha with its *rekha deul*, Bengal's terracotta temples, Kerala's sloping-roof temples) are (J) from background knowledge and not verified here; the table says so.

The element table is the fillable deliverable (section "Templates and deliverables", T2). Findings that shape it:

- A set is built from the axis: entrance, mandapa, antarala, garbhagriha. "Mandapas lie between the sanctuary and the temple entrance, on the same axis" [55]. The garbhagriha is dark and windowless (digest of a Smarthistory page [60]) and is where photography is most strictly forbidden (section F5, temple bodies), so it is drawn, never photographed.
- A mandapa is also the Hindu wedding pavilion in everyday speech [55], which makes it a candidate for her wedding set only if a real event and photograph exist.
- The gopuram is a frame device: a vertical, tiered, painted tower, "brightly-painted plaster" with a barrel-vaulted top and kalasam finials [54]. As a transition it is a tilt up the tiers, never a dissolve.
- A stepwell (vav, baoli; kalyani or pushkarani in Kannada) is a descent frame [59]. "Construction hit its peak during Muslim rule from the 11th to 16th century"; stepwells were "initially used as an art form by Hindus" [59], so each named stepwell is checked: Rani ki vav (Patan, Gujarat) and Chand Baori (Abhaneri) are named in the page but their dynasty and religion were not stated there, so the Hindu attribution is (J) and needs one more source before use.
- A torana is "a free-standing ornamental or arched gateway for ceremonial purposes" used in Hindu, Buddhist and Jain architecture; the Chaulukya toranas of Gujarat (10th to 12th centuries), such as the Kirti Toran at Vadnagar, were "mostly associated with temples"; a festive torana of mango leaves hung over a door is the same word and the same idea [56]. That the Gujarat toranas carry makara heads and a scalloped arch, and are the likely Hindu ancestor of the cusped arch, is (J) from background knowledge: the page read does not discuss it, so the arch stays on the exclusion list.
- Shared or ambiguous elements are the exclusion list (section "Exclusions and ambiguous cases", entries E1 to E8 for architecture).

### F5. Deities most likely to be hers: attributes, forms, marks and who controls the image

The checklist (T3 below) is built from Gopinatha Rao's *Elements of Hindu Iconography* (1914; Vol I Pt I, Vol I Pt II, Vol II Pt II; full text read from archive.org) [61][62][63], cross-checked against Wikipedia deity pages read on 2026-10-19 [64] to [78]. Rao collects agamic and puranic descriptions and says openly where they disagree; he is also a 1914 colonial-era scholar whose historical claims (a "Buddhist relic" in the Jagannath image, Tirumala as "Harihara") are contested and are **not repeated here** [61]. The pages truncated at 100,000 characters (Ganesha, Lakshmi, Saraswati, Durga, Kali, Hanuman, Shiva, Vishnu, Krishna, Rama) were read only up to that cut; sections beyond it are UNVERIFIED.

**Marks (S).** Vaishnava *urdhva pundra*: "two or three vertical lines ... crossed in the middle by an elongated U" [74]. Shaiva *tripundra*: "three horizontal bands across the forehead with a single vertical band or circle in the middle", made of vibhuti [74]. Shakta: "a red dot ... in the middle of three horizontal lines or a semicircular line" [74]. Ganapatya: red sandal paste [74]. Jagannath wears the vertical urdhva pundra [70]. The Tenkalai (Y) and Vadakalai (U) Sri Vaishnava namam forms are not in the page read [74]: (J) from background knowledge, ask her image.

**Which temple bodies assert control over their deity's image (dated).**

| Body | What I found | Date | Source |
|---|---|---|---|
| Shree Jagannath Temple Administration (Puri) | Police complaint at Singhadwar police station against an account for AI images and videos of the deity, including a video of milk poured over the deity "using a crane"; the administration said it was "the first known instance" of AI used this way; its managing committee decided to amend legal provisions to make such acts offences | 20 to 21 Jan 2026 | [83][84] (Organiser has a "nationalist" slant and relies on the temple's account) |
| Tamil Nadu HR&CE (state temple department) | Phone limits eased 11 Oct 2026 (phones allowed if switched off); "photography and video recording" remain banned in temple premises, with a fine | 11 Oct 2026 | [86] |
| Tirumala Tirupati Devasthanams | No notice on AI images found. Digest only: a warning against filming social-media reels (31 Jul 2025) and a vigilance officer saying private cameras are not allowed near the temple (2022) | UNVERIFIED | [87 digest] |
| Nathdwara (Shrinathji) | Governed under the Nathdwara Temple Act; the Supreme Court upheld it in 1963 against the Tilkayat's claim that the idol was private property (digest only). No image-rights rule found | UNVERIFIED | [90 digest] |
| Hindu American Foundation | Guidance that AI images are not sacred and correctness matters; commercial-use "don't" and "caution" lists | 6 Oct 2025, updated 24 Oct 2025; commercial guidelines undated | [79][80] |
| South African Hindu Maha Sabha Priests' Council | Called AI images of a man holding hands with Ganesha, Hanuman, Krishna and Lakshmi "blasphemous": "Any attempt to present humans as equal to Gods via digitization would be offensive" | about 2024 (the page says "2 years ago") | [85] |

So: a murti photograph taken in a temple is out as a source (the maker's own photograph of her home shelf is the exception), and the one temple body that has acted on AI deity images is Puri.

### F6. What practitioners and devotional animators treat as disrespectful

Sources: HAF's commercial-use guidelines [80]; the Hindu American Foundation AI essay [79]; the South African priests' council [85]; the Puri complaint [83][84]; Rao on poses and groups [61]; the 1992 and 2023 controversies [91][93]; the arXiv interview study of 15 Bangladeshi Hindus (June 2024 to April 2026; the paper does not name the models) [81]; the University of Zurich blog post of 21 Aug 2026 [82]. The twenty shot rules are in T4 below. What the sources say, in short:

- **Feet and the ground.** HAF's "don't do it" tier: footwear "of any type", door mats and rugs, bath mats, toilet items, underwear, swimwear, alcohol and meat, yoga mats and skateboards, "anything where the image is likely to be destroyed through normal intended usage, intended to be stepped upon". Its "caution" tier: towels, mouse pads, items "likely to get regularly dirty", and items that "significantly modify a deity" such as non-traditional objects in Nataraja's hands. HAF adds that intent matters and that "outside India" the understanding may not exist [80]. The guidelines page gives no footwear-specific reason; a search digest of a 2015 HAF letter says feet "are considered unclean" through contact with the ground, which I could not open.
- **A human next to a deity.** The 2024 South African case: AI images of a man walking hand in hand with Hindu deities in ripped jeans and sneakers; critics objected to "a human appearing beside deities", the sneakers and the casual clothing [85].
- **Casual or comic treatment.** The VHP objected in the 1980s to gods being "drawn as cartoon figures" and the Indian government declined collaboration on the 1992 film, calling the subject "too sensitive for cartoons" [91]. *Adipurush*: slang in the mouths of gods, a Ravana in "leather jackets", a poster where the characters "were shown without the sacred thread (janeu)" [93].
- **Fabricated ritual.** The Puri complaint is specifically about a ritual that "never happened" [83][84].
- **Placement and discard.** "Images on discarded items" is a practitioner concern (invitations, calendars, firecracker labels) but I found no authoritative ruling: a digest of a Pushtimarg devotional page asks how to dispose of such images "without feeling bad or guilty" and gives no ruling [108]. Treated as (J).
- **Skin colour, sexualisation, aggression.** Participants objected to a "very white" Rama, to goddesses "sexualized and exoticized", and to an "aggressive or always angry" Hanuman [81].
- **Dissolve or wipe as a transition, a deity cut at the neck by the frame.** No source found; these are the brief's leads and Fable's, written as (J) rules that follow from "do not treat the image casually or destroy it". The maker can overrule with knowledge.
- **A lamp blown out.** (J), the brief's object list; no source.

### F7. AI image and video for deities: failure modes, reactions, the safe route

- **Documented failure modes (S).** Complexion (Rama rendered "very white", "not a small artistic mistake"), sexualisation of mother goddesses, an always-angry Hanuman, tantra as "satanic or hypersexual visuals", a Brahmin in a pagri, misrecognition (the saint "Ramthakur" answered as Rama) [81]; mixed-in Tibetan Buddhist elements and stylistic changes, with the risk that errors "could spread and eventually be treated as correct by future AI models" (HAF) [79]; a Rama image controversial for looking "too feminine" (a one-line mention, no date or source) [82]; fabricated rituals (Puri) [83][84]. The 2025 "Ghibli-style" ChatGPT trend (Axios, 26 Mar 2025, digest only) [89]: no Hindu-organisation objection to Ghibli-styled deities was found; UNVERIFIED.
- **Not measured:** miscounted arms, swapped attributes between deities, wrong vahana, malformed hands and feet, glossy gold. They are the failures an iconography sheet can test by counting, which is why the checklist is count-based. UNVERIFIED as AI-specific findings.
- **Community position (S).** HAF: a worship image should be "an interpretation of the dhyana mantra, a meditative visualization"; "As AI has no capacity to meditate, it cannot tap into the aspects of reality that humans can access in this way"; "AI images are not inherently sacred"; a limited exception for rare deities "prompted from the dhyana mantra and refined carefully for iconographic accuracy"; decorative use such as phone wallpapers is outside the guidance [79]. The interview study found AI acceptable as a bridge to scripture and a visualisation aid, unacceptable when deity images "speak" non-scriptural advice [81].
- **Safe route (J on S).** (1) Symbols first (aniconic is normal in Hindu homes: lamp, kalash, lotus, conch, Om, linga, padukas); (2) agent-drawn vector symbols checked against the sheet; (3) hand-traced public-domain plates with `deity_source`, plate id and licence text logged and the L3 label; (4) the maker's own photograph of her home shelf, `cloud: none`; (5) a commissioned painting with a written licence. AI clean-up of a deity plate is allowed only as non-generative scaling or tonal work, logged L1 or L2; diffusion repair of a deity plate is banned because it can silently change an attribute. The maker reviews every deity drawing as her proxy (W-40).

### F8. Rights per source and per jurisdiction

The excerpts are saved in `research/sources/hindu-visual-licence-excerpts-2026-10-19.txt`. The route table is T5 in "Templates and deliverables". Findings:

- **Holdings and terms in one line each (S, dated 2026-10-19).** Cleveland: CC0 for images and data, with exclusions (not fully owned, restricted by artist, donor or lender), launched January 2019; keyword hits with `cc0=1` give an order of magnitude only (Pahari 125, Krishna 160, Vishnu 85, Shiva 97) [1][3]. Met: data CC0, "images are not included"; the images page returned 429 so image terms are digest only; v1 of the search API retired on 2026-10-01 and v1.1 replaces it; Tripe's 1858 Madura gopuram photographs are flagged public domain [4][5][6]. Smithsonian: CC0 at record level for National Museum of Asian Art objects (for example `fsg_S2018.1.3`, c. 1740 Krishna Vishvarupa), repository archived 21 May 2026; the website was blocked [7][8]. AIC: data CC0, "does not contain image files", "it is up to you to determine whether or not you are allowed to use these images" [9]. LACMA: public-domain downloads "free of charge and for use without restriction", credit the artist and "www.lacma.org", protected content "limited non-commercial personal use" [10]. Rijksmuseum: "Public Domain or Creative Commons Zero", credit requested, some restrictions [11]. Philadelphia: images "generally of artworks in the public domain", no licence name [13]. Harvard: "personal, noncommercial use, including educational and scholarly purposes" [12]. V&A: free for non-commercial use, commercial through the image licensing team [16]. British Museum: CC BY-NC-SA 4.0 per digest [17]. San Diego: nothing found [18]. Google Arts & Culture: partner rights, view-only [19].
- **Wellcome Kalighat audit (M, dated).** 184 results for "Kalighat"; 96 digitised works with the Public Domain Mark, 81 with no online item, 4 CC BY, 3 CC BY-NC (including the Lakshmi plate `phr7cv3d`, "You can use this work for any purpose" but not "primarily intended for or directed to commercial advantage") [14][15]. A public screening, even free, may or may not be "commercial advantage": treat CC BY-NC as ask. The Public Domain Mark is Wellcome's statement about the painting; it does not answer whether the plate is respectful: titles include "Ganesh playing the dhola (double drum)", "Shiva sits on a tiger skin with sitar in hand" and "Two men carrying a captured monkey tied to a pole, possibly Hanuman" [15]. Every plate is screened against the shot rules.
- **Photographs of public-domain 2D art.** US: *Bridgeman v. Corel* (1999) held exact copies of two-dimensional public-domain art lack originality, "in the United States only" [20]. Commons accepts PD-Art from any country but warns "Reuse of {{PD-Art}} images may be restricted in some countries" and that arguments exist for England and Wales, Spain, the Nordic countries and Taiwan [20]. UK: IPO guidance of 4 Jan 2021 says "it seems unlikely" a faithful digitised copy is original but admits "a degree of uncertainty"; I found no 2023 change [24]. India: no case found on photographs of public-domain paintings; the originality test in *Eastern Book Co v D.B. Modak* is "not copied" with a minimal creative step (digest only) [28]. Raja Ravi Varma died 2 Oct 1906, so under s.22 his copyright ended with 1966 and he has been public domain in India since 1 Jan 1967 (arithmetic ours) [25]; the first Ravi Varma Press oleographs date from after 1894, the press was sold to Fritz Schleicher in 1901 and kept commissioning new designs [48], so each plate's artist and first-publication date are checked before it is called public domain.
- **Wikimedia Commons is file by file.** CC0: Kandariya Mahadeva (Ms Sarah Welch) [21] and a Hoysaleswara makara relief [22]; the same uploader's Ganesha photograph is CC BY-SA 4.0 (digest). PD-Art: the 1809 Bluck aquatint after Salt, "In other jurisdictions, re-use of this content may be restricted", source the British Library [23]. CC BY-SA means a traced adaptation must be shared alike, so it is reference-only for the film. UNVERIFIED: whether CC BY-SA obligations reach a film that uses a hand redrawing of a CC BY-SA photograph; ask in the T10 consult.
- **Not usable as sources:** Amar Chitra Katha panels (owned) [97]; murti photographs from temples where photography is banned [86]; temple-trust calendar art (assume owned); a living artist's Pinterest repost; a Google Arts & Culture zoom.

### F9. Commissioning a living traditional artist

- **Costs and lead times seen (search digests of marketplace listings, pages blocked with HTTP 429 on 2026-10-19, UNVERIFIED).** Pattachitra: 12 by 18 inch Jagannath INR 15,000, estimated delivery one to two weeks "including 1 week for hand-crafting"; 24 by 40 inch Ram Abhishek Darbar INR 26,000, estimated delivery one to two weeks in one listing and three to five in another. Tanjore: 15 by 12 inch with 22k gold foil INR 21,600, about one week to handcraft and two weeks delivery (one marketplace); a 42 by 54 inch framed 24k gold piece US$5,020 with the seller saying "at least one or two months" (another). Madhubani: sets from about INR 4,200 to INR 20,000, made to order "typically about two weeks". Custom size, colour and elements are "customised" by quote on WhatsApp or email, with no published price list [106][107]. No Srikalahasti or Phad price was found. Treat as an order of magnitude: INR 15,000 to 50,000 or more for a custom piece, six to ten weeks end to end including a sketch approval, painting, shipping, a 600 ppi scan and slack for festival season (J).
- **GI status and what it restricts.** Registered GIs I could read: Odisha Pattachitra 10 Jul 2008, Bengal Patachitra 28 Mar 2018 [30]; Cheriyal 2008 [39]; Thanjavur 2007 to 2008 [33]; Srikalahasti April 2005 and Machilipatnam April 2008 [41] (other sources give 2006 and 2009); Madhubani reported, year not read from a registry [31][51 digest]. Section 22 of the GI Act reaches use of the indication on goods that suggests a false origin or is unfair competition, and use "accompanied by expression such as 'kind', 'style', 'imitation'" for notified goods [27]. It does not make a painting style property and says nothing about depicting a style in a film. Practical rule (J, T10 question): do not sell prints or merchandise labelled with a GI name unless made by authorised users; credit honestly as "in the manner of" or "made with [artist], [place]".
- **Copyright and the written paper.** s.17: the author is the first owner; clause (b) gives a person who commissions "a painting or portrait" for "valuable consideration" first ownership "in the absence of any agreement to the contrary"; the proviso says that for a work incorporated in a cinematograph film, clauses (b) and (c) do not affect the author's s.13(1)(a) rights [25][26]. s.19: an assignment is valid only "in writing signed by the assignor"; it must identify the work, rights, duration and territory; "If the period of assignment is not stated, it shall be deemed to be five years"; territory unstated is presumed India only; rights lapse after a year unused unless the assignment says otherwise [25]. Consequence: a film licence or assignment must say worldwide (the premiere country is unknown, TD-7), a term that covers the April version and the archive (the register says copies are refreshed to 2032), all media including a phone file, and that the artist keeps the painting's other rights if that is the deal. UNVERIFIED: that the Indian Kanoon text is current. The T10 list gets five added questions (T8 below).
- **A name-free brief (D-03, D-07).** "A devotional painting of [form named from the sheet] in the [tradition] manner, [size], for a private film project to be shown publicly in 2027; no names; the film use will be licensed in writing; delivery date; we need a high-resolution scan or photograph taken by you for the licence." Whether telling an artist that a film exists is acceptable under only-me is the maker's call (open question V5). Use a gallery or cooperative as the intermediary where possible.

### F10. What agents can build as seekable SVG scenes (Route A, W-23)

Existing rules: a scene exposes `window.seekTo(t)`; ids on every moving element; pivots in `data-pivot`, stacking in `data-z`; VectorCraft "keeps ids and `data-*` attributes" and "drops `class` attributes, `<style>` text, most filters, SMIL and CSS animation, and transforms on groups" [agent-pipeline][craft-visual]. Line-draw uses `stroke-dashoffset` against `pathLength`, per MDN [toolchain [66]]. Matrix (T7) in the templates section.

- **Parametric floor art.** A pulli grid and a closed stroke around dots (sikku) is the traditional construction [45]; mathematics of kolam is a research field (Siromoney; Ascher) [45]; an existing R toolkit stores kolams as gesture codes under AGPL v3 [50], which we read for method only and do not link or copy. Agents write their own generator when code is allowed.
- **Cut-out puppets.** Four to twelve joints [44], heads detachable [44], so a layered SVG with a `data-pivot` per joint matches the form. The hole minimum (4 px) governs how much perforation the drawing may keep.
- **Vector symbols.** Torana, kalasha, amalaka, lotus, diya, Om, conch, chakra, trishula, veena, vel, bell: agents draw and the sheet checks; the maker approves.
- **Needs a human hand.** Any deity figure; Kalighat and Pattachitra faces; Tanjore gold relief; Madhubani figure fields; anything meant to look like her own hand-made material.

---

## Exemplars and what they teach us

1. **Separate registers by medium, not by filter** (*Sita Sings the Blues*) [92]. The look changes where the function changes (picture, narrator, song), which is W-38's rule that the look changes where the photographer changes. Take the method; take no assets. The film was an outsider's retelling and drew a petition; ours is a family's tribute to a Hindu mother, which changes the standing but not how images are judged.
2. **Cartoon gods are contested for some devotees** (1992 film: VHP objection; government "too sensitive for cartoons") [91]. This is why deities on screen is a question for the maker as her proxy (O-42) and not a team default. The mitigation the successful films share is scriptural fidelity and ritual restraint (*Mahavatar Narsimha* names its Puranas and visits Ahobila) [94] rather than a house style.
3. **Casual register fails** (*Adipurush*): slang, costume liberties, uncanny VFX, a missing sacred thread [93]. For us: no jokes in the deity's mouth, no comic timing on a deity, correct marks.
4. **Craft with a practising hand beats imitation** (Sabnani) [100]: the artist is a collaborator and is credited; the craft's tactile quality survives. Under only-me this becomes "buy a piece, licence it in writing, and draw our own world around it".
5. **Painterly takes years** (*Bombay Rose*, about six years, digest) [101]. At 19 weeks the film uses a painted or drawn plate plus small moving parts, not frame-painted animation.
6. **Game-like 2D stiffness fails** (*Arjun*) [96]. Stillness with one clear move is the project default anyway (animated.md decision 2).
7. **Personal framing is what a mainstream short built its deities on** (*Sanjay's Super Team*: the director's childhood puja) [98]. Her shelf, her lamp, her hands first; a deity figure only if the shelf has one and she would welcome it.
8. **Floor to stay above**: *Chhota Bheem* (not researched, UNVERIFIED) and Amar Chitra Katha's printed canon, whose look the audience will bring to any Hindu animation [97].

---

## Templates and deliverables

### T1. Style-options matrix (scored; gate first, then rank)

**Gate before scoring.** A tradition is eligible only if all three are true: (a) D-28 flag is OK or OK-note, not FLAG or OUT; (b) it is hers: her region (O-36), her sampradaya (O-37) or her hands (O-40) calls for it, or it is a floor art of her region; (c) it can be drawn at the phone floor (T6 `idiom_line_px_1080`) without losing its identity. Scoring is only for ranking the eligible ones. Until O-36 to O-40 are answered every row is "hers if" and nothing is chosen.

**Scores 1 to 5, five is best.** Meaning = how much of a specific, domestic life it can carry if it is hers (J). Motion = how naturally it breaks into moving parts (J on the sourced conventions in F1). Phone = from the fixture and the identity features in F3 (M, then J). Big screen = richness at 10 m (J). Effort = how little hand work an agent-plus-maker team needs (5 is least; J, hours per 10 s shot not measured). Rights = how clean the route to drawing in the manner is (J on F8; the style itself is free, the plates and living artists are the question). Weighted total = Meaning x2 + Phone x2 + Motion x1.5 + Effort + Big screen + Rights, out of 40. Weights are mine; change them with the maker.

| # | Tradition | Hers if (the unknown) | Mean | Mot | Phone | Big | Eff | Rights | Total /40 | One-line reason for the scores |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Floor arts: kolam, muggu, rangoli, alpana, mandana, aipan, jhoti, pookalam | Her region (O-36) or her hands (O-40) | 5 | 5 | 4 | 4 | 5 | 5 | **39.5** | Daily, domestic, drawn by her hands; line-draw is native; cream-on-dark lines hold from 3 px (M); pulli grids are parametric; traditional patterns carry no plate or GI problem |
| 2 | Kalighat (Bengal) | Bengal, Shakta household (O-36, O-37) | 4 | 4 | 5 | 4 | 3 | 5 | **36** | Bold single-sweep outlines survive recompression; limbs cut cleanly; a Wellcome "Kalighat" search returns 96 Public Domain Mark items; but also satirical, so every plate is screened (R18) |
| 3 | Shadow puppet cut-out (Tholu Bommalata, Togalu Gombeyaata) | Andhra, Telangana, Karnataka (O-36) | 3 | 5 | 4 | 5 | 4 | 4 | **34.5** | Four to twelve joints is hinge animation; backlit colour glows on a big screen; perforations close below 4 px (M); epics more than domestic life; Togalu costume flagged |
| 4 | Phad and Cheriyal scroll | Rajasthan (Phad), Telangana (Cheriyal) | 4 | 4 | 4 | 4 | 3 | 3 | **32** | A life as panels told by a storyteller fits the structure; red-ground primary colours and large figures hold; dense Cheriyal panels fail; Phad is a Joshi family craft, so commission or credit |
| 5 | Kerala temple murals | Kerala (O-36), temple or palace family | 3 | 3 | 4 | 5 | 3 | 4 | **30.5** | Five flat colours and thick outline hold; guna colour is meaning and must not be recoloured; hieratic figures move little; the Mattancherry set has a palace history |
| 6 | Pattachitra (Odisha) | Odisha, Jagannath devotion (O-36, O-38) | 3 | 3 | 3 | 4 | 3 | 4 | **27.5** | Angular line and the red ground are strong, the fine border is not; the border must stay still; living artists and a GI |
| 7 | Madhubani (Mithila) | Bihar, Mithila; she painted or her house walls were painted | 4 | 3 | 2 | 4 | 2 | 4 | **26.5** | Women's domestic art and the kohbar wall suit a life; "no space left empty" and hatching fail on a phone (M) unless redrawn coarse (3 px at 9 px pitch) |
| 8 | Tanjore and Mysore gilt gesso | Tamil Nadu or Karnataka; a Tanjore painting on her wall | 3 | 2 | 3 | 5 | 2 | 4 | **26** | Gold relief is the best big-screen material and the worst phone material; static icon; "seraphs" omitted; Mysore finer than Tanjore |
| 9 | Kalamkari (Srikalahasti only) | Andhra, temple cloth in the family | 3 | 3 | 2 | 4 | 2 | 3 | **23.5** | Pen line is the identity and falls under 3 px (M); GI and guild; Machilipatnam is out |
| 10 | Nathdwara pichwai | Pushtimarg household only (O-37) | 2 | 2 | 3 | 5 | 2 | 3 | **23** | Backdrop for Shrinathji; dense lotus and cow repeats go to mush; wrong outside Pushtimarg |
| 11 | Pahari / Kangra and Rajput court (FLAG) | Only if the maker overrules E-entry 10 | 2 | 2 | 2 | 5 | 1 | 5 | **22** | Lovely, courtly, hairline, Mughal-trained origin; plenty of CC0 plates; lowest fit |
| n/a | Raja Ravi Varma | A deity-plate source, not a style | | | | | | 4 | | Public domain by author's death (India 1 Jan 1967) but plate by plate; naturalistic, so uncanny if animated; used as a still plate under the respect rules |

**Collapse rule (what the table becomes once O-36 and O-37 are answered).** One to three rows survive: for example Tamil Nadu gives rows 1 and 8 (kolam, Tanjore), Bengal rows 2 and 1 (Kalighat, alpana), Odisha rows 6 and 1 (Pattachitra, jhoti), Mithila rows 7 and 1 (Madhubani, aripana), Andhra rows 3, 1 and 9, Karnataka rows 3, 1 and 8, Rajasthan rows 4, 1 and 10 only for Pushtimarg, Kerala rows 5 and 1. Where the maker's own hands made a craft, that craft is the primary tradition whatever its score (decision 2 and 11 are one thing).

### T2. Temple-architecture vocabulary: element table

| Element | Order | Plain definition (S) | Silhouette to draw | Film use | Open reference image (licence, read 2026-10-19) | D-28 note |
|---|---|---|---|---|---|---|
| Shikhara | Nagara | "Mountain peak", the tower over the sanctum; latina (four faces, curved), sekhari (attached spirelets), bhumija (grid of miniature spires) [53] | Curvilinear beehive, ribbed, rising to a disc | A tilt-up frame; set for a northern household | Kandariya Mahadeva temple, Khajuraho, CC0, Ms Sarah Welch, 4,400 x 3,300 [21] | Khajuraho invites the "erotic temple" stereotype in a public room: silhouette only (J) |
| Amalaka and kalasha | Nagara (and Dravida finials) | Disc-stone then urn at the top "by at least 600 CE in Odisha" [53]; kalasam finials on gopurams [54] | Ribbed disc under a pot with a point | Finial motif; the domestic kalash (pot, mango leaves, coconut) is a related shape (J) | None verified | Not a dome |
| Vimana | Dravida | The tiered pyramidal tower over the sanctum [52][54] | Stepped pyramid, each tier smaller, domed cap | Axis set; vertical push | Thanjavur temple, aquatint by John Bluck after Henry Salt, 1809, PD-Art, British Library [23] | None |
| Gopuram | Dravida | Monumental entrance tower; levels called tala; "usually brightly-painted plaster"; barrel-vaulted top with finials [54] | Tapering tiers with rows of figures, horizontal bands | Tilt up the tiers; module card frame; never a dissolve | Linnaeus Tripe, 1858, Met Open Access, public domain flag: 287277 "The Western Gopuram", 287268, 287267 "Madura: The Roya Gopuram from the East" [5] | The Met titles say "Pagoda" (colonial term) |
| Mandapa | All | Pillared hall for public ritual; ardha, maha, ranga (dance), kalyana (the deity's wedding), a thousand-pillar hall; lies "between the sanctuary and the temple entrance, on the same axis" [55] | Rows of pillars in perspective | Wedding set only if a real photograph exists | None verified (Commons has Tripe's portico pillars, licence template not seen: UNVERIFIED) | None |
| Garbhagriha | All | "Womb chamber" sanctum [52]; dark, windowless (digest) [60] | A dark square with one lamp | Drawn, never photographed | None; photography is banned inside most sanctums [86] | None |
| Antarala and pradakshina | All | Vestibule; the clockwise circumambulatory path [52] | A corridor around a block | Camera path: clockwise (J) | None | None |
| Torana | All | Ceremonial gateway; Hindu, Buddhist and Jain; Chaulukya toranas "mostly associated with temples"; mango-leaf torana over doors [56] | Two posts and a curved lintel | Door and module-break frame; the festive leaf torana is the domestic one | Kirti Toran, Vadnagar, CC BY-SA 3.0 (digest only) | Cusped arch ambiguity (E2) |
| Makara | All | A fused beast: peacock tail, lion body, crocodile mouth, insect or boar snout [22] | Curled beast head | Ornament on toranas and thresholds | Hoysaleswara makara relief, CC0, Ms Sarah Welch, 4 Sep 2017 [22] | None |
| Dvarapala | All | Door guardian | Standing figure with club | Frame the threshold | None checked | None |
| Stepwell, tank | Western and Southern | Vav, baoli; kalyani or pushkarani in Kannada; a long corridor of steps to water [59] | Zig-zag of steps | A descent frame | None CC0 found; CC BY and CC BY-SA files exist (digest) | "Construction hit its peak during Muslim rule from the 11th to 16th century" [59]: check each |
| Vesara (Chalukya-Hoysala hybrid) | Vesara | Mixes Nagara and Dravida features; Lakkundi, Dambal, Itagi, Gadag; Hoysalas continue [52] | Stepped but starry plan (J) | Karnataka households | Hoysaleswara makara only [22] | None |
| Kalinga rekha deul | Nagara sub-style (J) | "The sanctum and the tower over it" in Odisha [53] | Tall curved tower with a pillared porch (pidha) (J) | Odisha households | None verified | None |
| Kerala and Bengal temple types | Outside the trio (J) | Not researched | | | | Ask |

### T3. Iconography do/don't checklist (form-first)

**How to use.** (1) The shot brief names one form (for example "Gajalakshmi", "Keshava", "Dakshina Kali"). (2) The implementor copies the default below, then replaces it with her own shelf image if O-38 supplied one. (3) The agent counts arms and attributes and reads the hand order; the maker counts again. (4) Anything marked "ask" goes to the maker in one line. Sources: Rao (1914) [61][62][63] for agamic descriptions and the "ask" disagreements; Wikipedia pages [64] to [78] for modern forms; marks [74].

| Form | Default attributes (S) | Do | Don't | Ask her image |
|---|---|---|---|---|
| Ganesha (Vinayaka, Pillaiyar) | Elephant head; usually four arms: axe or goad and noose above, a broken tusk and a sweet below [64]; large belly; snakes as sacred thread and belt [61]. Trunk "generally ... towards the left"; right is rare and Tamil "Valamburi" [61]. Exactly one tusk broken; the Brahmanda Purana says the left, "a large number of sculptures" lack the right [61]. Mouse; peacock (Mayureshvara); lion (Vakratunda) [64]. Red or white [64]. Red sandal mark [74] | Name the form; copy her trunk and tusk sides | Two whole tusks; a mirrored asset; a dancing or drumming Ganesha (a satirical Kalighat subject exists [15][29]) | Trunk side; Pillaiyar or Ashtavinayak form [64] |
| Lakshmi, Gajalakshmi | On a lotus; two hands beside Vishnu, four when alone: long-stalk lotus, bilva fruit, amrita pot, conch (Silparatna) [62]; popular: lotus in one or two hands, wealth poured from a hand [65]; Gajalakshmi: two elephants pour water from pots [62][65]; owl occasionally [65]; golden, red dress with gold thread; smaller than Vishnu beside him [65] | Name the consort or Gajalakshmi form; elephants pour from pots | Disc halo, winged attendants, a Western coin stack, a lamp blown out in front | Kolhapur Mahalakshmi (child-like, linga on head, four hands) [62]; Ashtalakshmi [65] |
| Saraswati | White lotus, white skin and clothes; four hands; the versions differ: rosary, vyakhyana mudra, book, white lotus (Amsumadbhedagama); a veena (Vishnudharmottara); goad, veena, rosary, book (Devi Mahatmya) [62][66]; hamsa, sometimes peacock [66] | Name which text; veena when the form holds one | A sitar (a flagged shared instrument and not hers) | The dancing eight-armed Hoysala form [62][66] |
| Durga (Mahishasuramardini) | Ten hands (Silparatna): right: trident, sword, shaktyayudha, discus, bow; left: noose, goad, shield, axe, bell; right foot on the lion, left touching the buffalo; three bends [62]; "a lion or a tiger" [67]; calm face in battle [67]; Bengal family group with Lakshmi, Saraswati, Ganesha, Kartikeya [67] | Name the form; show symbols (trident, lion, lotus) if the figure is not on her shelf; the textual blood is not drawn | A lion where her region has a tiger; eighteen arms (a Vaishnava form) unless named [67]; swapped weapons | Lion or tiger; eight, ten, eighteen arms; the Navadurga set [67] |
| Kali | Dakshina Kali: four arms; sword and severed head left, abhaya and varada right; garland of 51 or 108 heads; skirt of arms; right foot on Shiva's chest; black or blue [68] | Bengali household only, and only if she keeps the figure; otherwise symbol | A Bengal Kali for a Tamil family (Bhadrakali and Mariamman are other forms, UNVERIFIED) [68]; drawn nakedness or gore | Whether the figure appears at all (default: no) |
| Annapurna, Parvati | Rao: red complexion, round face, three eyes; a vessel with honey in the left hand and a spoon with rice in the right; four-handed: noose, goad, abhaya, varada; crescent on the crown [62] | Pot and ladle on the kitchen shelf (W-34) | Lakshmi's owl or lotus on Annapurna | Kashi form or the household form [62] |
| Shiva | Usually worshipped as the aniconic linga [75]; third eye, crescent, Ganga from the matted hair, Vasuki, trident, damaru, blue throat, tiger skin, Nandi [75]; tripundra of vibhuti [74] | The linga as the primary form in a Shaiva home | A Vaishnava U mark; "non-traditional objects in a deity's hands" (Nataraja example) [80] | Nataraja, Dakshinamurti, Ardhanarishvara [75] |
| Vishnu (24 forms) | Four arms: conch, discus, mace, lotus; the form's name depends on which attribute is in which hand, read upper right, upper left, lower left, lower right: Keshava is conch, discus, mace, lotus [61]; Garuda; Shesha bed with Lakshmi [76]; U mark [74] | Write the hand order into the brief | Mirror the asset (it reverses the order and changes the form); an unnamed "Vishnu" | Narayana, Govinda and the rest are other permutations [61] |
| Krishna | Dark or blue skin; peacock feather; flute; tribhanga; cows and calf; Radha; Bala Krishna, Makhan Chor, Laddu Gopal; Govardhana [77] | Child form if that is on her shelf | A Pushtimarg Shrinathji in a non-Pushtimarg home [38]; the clothes-stealing episode and comic butter gags (screen) | Laddu Gopal or Radha-Krishna on the shelf |
| Rama, Sita, Lakshmana, Hanuman | Rama dark, bow left and arrow right [78]; in Rao's bronze groups Rama's right hand is lowered "as if to receive an arrow", left raised on the bow; Hanuman stands in front and to the right with two hands, right on the mouth, left hanging, a servant's posture; Sita's right hand hangs, left in kataka; Lakshmana like Rama [61]. Sources disagree on Sita's side (Rao, for a 16th to 17th century bronze group: left of Rama; Wikipedia: right) [61][78] | Copy her group; Hanuman beside, never above | A four-armed Hanuman (Panchamukha has five faces, ten arms and is its own form [69]); Hanuman larger than Rama | Ramaparivar or coronation group; Sanjeevi (mountain) Hanuman [69]; Sita's side |
| Murugan (Kartikeya, Subrahmanya) | Spear (vel), peacock, rooster banner; usually one head, six in Shanmukha [73]; Rao: Shanmukha six faces, twelve eyes, twelve arms, saffron, on a peacock [63]; Valli and Devasena in Tamil tradition; Palani ascetic form [73] | A Tamil family: Valli and Devasena; her abode among the Arupadai Veedu [73] | A "celibate Kartikeya" for a Tamil family [73]; Rao's 1914 remark that women in some regions avoid him is dated, ask [63] | Which abode |
| Ayyappa (Sasta, Ayyanar) | Seated young man in a yogic posture, bell at the neck, bow and arrow, tiger [72]; Rao: Sasta on a white elephant, cock banner, shrine at the south-west corner of Kerala temples [63] | The 18 steps imagery | The Vavar mosque pairing in the pilgrim story (out, E18); Ayyanar village forms unless hers [72][63] | Kerala or Tamil form |
| Venkateswara (Balaji, Srinivasa) | Standing, four arms on a lotus: conch and discus above, one hand varada, one on the hip; Vyuha Lakshmi on the chest; naga ornament; diamond crown [71]; the U-shaped namam [74] | Namam shape from her image | Any murti photograph from the sanctum; Rao's 1914 "Harihara" reading (contested, not repeated) [61] | Tenkalai or Vadakalai namam (J) |
| Vitthal (Pandharpur) | Standing, two hands on the hips, feet on the ground; kirita with a linga mark per Rao; Rukmini beside [61] | Plain form | Added attributes | Whether on a brick (J) |
| Jagannath, Balabhadra, Subhadra, Sudarshana | Neem log; square flat head; no neck, ears or limbs (two stumps in some modern temples); two large round eyes without lids; Jagannath dark, Balabhadra white, Subhadra yellow, Sudarshana red; Jagannath's eyes circular, the others oval; vertical U mark [70] | The abstract form and the triad order | Arms, legs, a human nose or mouth ("some paintings outside India show him fully anthropomorphized" [70]); any AI image or video [83][84]; Puri murti photographs | The Pattachitra convention if Odia |
| Regional mother goddesses, kuldevi | No standard form; not researched (J: often a stone, pot, mask or coin) | Follow the shelf | Substituting Durga | Everything |

**Marks.** Vaishnava: vertical lines with an elongated U [74]. Shaiva: three horizontal bands with a vertical band or circle [74]. Shakta: red dot with three lines or a semicircle [74]. Ganapatya: red sandal [74]. Never put one sect's mark on another's deity; never a mark on a deity whose sheet row has none.

**Whole-sheet rules.** One named form per shot. Count arms and attributes against the row and her image. Never mirror. Skin colour by form. A flame arch (prabhavali) or the form's own aureole, not a disc. A lotus seat is a lotus. A lamp is lit.

### T4. Respect rules as shot rules (twenty, checkable)

"Auto" means the timeline validator can check a field; "agent" and "maker" are counts or looks. The maker approves every deity drawing as her proxy (W-40); Fable flags; default OUT on any doubt (D-04).

| ID | Rule | Check | Basis |
|---|---|---|---|
| R1 | A deity image is never on a surface that is walked on, sat on, stepped over or discarded: floor, rug, step, shoe, plate, packaging, bin, torn paper | agent, maker | HAF "don't" tier [80] |
| R2 | No foot, shoe or sole points at or touches a deity image; no deity image below a person's knee height in the frame except a floor shrine drawn with the person seated or kneeling before it and the feet tucked | agent, maker | [80]; framing (J) |
| R3 | No footwear in a frame with a shrine, a deity image or a lamp before a deity, unless it lies at the threshold | agent | [80]; etiquette (J) |
| R4 | A deity figure is never cropped through the neck or waist; a crop to a hand or an attribute needs the maker's yes; the full icon is held at least once per appearance | agent | (J) |
| R5 | No dissolve, wipe, burn, shatter, pixelate, fade-through or morph on a deity image; entry and exit by cut or a lamp-lit hold | auto (`transition` field) | (J); cinematic-quality T9 row 3 |
| R6 | No squash and stretch, bounce, wobble, shake, speech, laughter, joke timing or comic sound on a deity; no beat-synced punch | agent | [91][93]; T5 item 8 |
| R7 | No non-uniform scale, skew, perspective warp, lens distortion, blur-as-effect or mirroring of a deity asset | auto (`transform` flags) | [61] hand order |
| R8 | Marks and skin colour follow the form: Rama, Krishna, Vishnu dark or blue; Kali black or blue; a Vaishnava U never on Shiva; tripundra never on Vishnu | agent | [74][65][68][81] |
| R9 | A person and a deity image share a frame only as darshan: the person at the side or lower, still, facing the shrine, hands folded or holding a lamp; never touching, never hand in hand, never at the same level and scale, never both walking | agent, maker | [85] |
| R10 | Arms, attributes and hand order counted against the sheet and her image, by the agent and again by the maker | agent, maker | [61] |
| R11 | A ritual is shown only if it happened or is a standard form she keeps | maker | D-16; [83][84] |
| R12 | Drape and ornament follow the form; no sexualising; iconographic nakedness and gore (Kali, Chamunda, the buffalo's neck) are not drawn: use the symbol | maker | [81] |
| R13 | Gold is flat or baked matte-bright foil; no glossy plastic gold, glow, flare or filter | auto (`filter` count 0) | (J); T5 item 4; VectorCraft drops filters |
| R14 | A flame arch or the form's own aureole, never a disc halo; no wings on apsaras or attendants; no cherubs; no candle where a diya belongs | agent | brief (J), UNVERIFIED per plate |
| R15 | A lamp before a deity is never blown, snuffed or faded out within the shot; a hand may shield it | agent | (J) |
| R16 | No meat, alcohol, leather or footwear in a shrine frame | agent | [80] for products; frame (J) |
| R17 | Deity images come only from: agent-drawn vector symbols checked against the sheet; hand-traced public-domain plates with plate id and licence text logged; the maker's own photograph of a three-dimensional murti on her shelf; a commissioned painting under a written licence. Never a temple murti photograph, a stock or Pinterest image, or anything AI-generated or AI-altered | auto (`deity_source` field) | [79][83][84][86] |
| R18 | A public-domain plate is screened for satire and irreverence before use | maker | [15][29] |
| R19 | A deity's name on screen is spelled in her script and checked against a printed source; no words put in a deity's mouth | maker | [81] |
| R20 | A deity symbol keeps the phone floor (4 px strokes, 6 px dots) and is never so small the form cannot be read; no deity in the bottom third of the frame while a person is in the top | agent | M-H1; (J) |

### T5. Rights route for every image source

Licence text per source is in `research/sources/hindu-visual-licence-excerpts-2026-10-19.txt`. "Route" is what the film may do. Every row needs a T8 line with the object's own page text saved and dated (W-46).

| Source | Hindu-relevant holdings (counts are keyword hits, order of magnitude) | Licence as read | Route | T8 type and status | Trap |
|---|---|---|---|---|---|
| Smithsonian NMAA via Open Access | Image records: Krishna 21, Devi 6, Vishnu 12, Shiva 9, Pahari 11 [8] | Record-level "CC0" [8] | Reuse or hand-trace; credit as courtesy | `artwork`, GRANTED after the record is saved | The record carries the licence, not the website; site blocked to our tools |
| Cleveland | Pahari 125, Krishna 160, Vishnu 85, Shiva 97 (keyword hits) [3] | CC0 for open-access items with exclusions [1][2] | Same | `artwork`, GRANTED | Third-party mirrors (digest: Photo12) are rights-managed copies |
| Met | Tripe's 1858 gopurams; an ivory Rama group (sculpture) [5] | Data CC0; images "CC0 icon" (digest) [4][6] | Same | `artwork` | Search API v1 retired 2026-10-01 |
| Art Institute of Chicago | Not counted | Data CC0; images "up to you" [9] | Only items tagged public domain | `artwork`, VERIFY | IIIF returns non-public-domain images too |
| LACMA | "The Hindu Gods Vishnu, Shiva, and Brahma" (digest) | Public-domain images "for use without restriction", credit the artist and www.lacma.org [10] | Same | `artwork`, GRANTED with credit | "Protected content" is personal non-commercial |
| Rijksmuseum | Not counted | "Public Domain or CC0"; CC BY 4.0 elsewhere; credit requested [11] | Check each item | `artwork`, VERIFY | South Asian holdings not stated |
| Philadelphia Museum of Art | Not counted | Images "generally of artworks in the public domain"; no licence name [13] | Treat as VERIFY | `artwork`, VERIFY | Assume rights unless an item says public domain |
| Wellcome Collection | 184 Kalighat results: 96 Public Domain Mark, 3 CC BY-NC, 4 CC BY, 81 no image [14][15] | Per work; Lakshmi plate CC BY-NC 4.0 [14] | PDM plates after screening (R18); NC and BY: ask or avoid | `artwork`, per plate | Public domain does not mean respectful |
| Harvard Art Museums | Not counted | Personal, noncommercial, educational [12] | Out unless a licence request is granted (a free licence "up to 6 weeks", digest) | VERIFY | |
| V&A | Largest Kalighat holding (645 paintings) [29] | Free for non-commercial; commercial via image licensing [16] | Ask in writing | `artwork`, ASK | A free premiere might still be "commercial" to them |
| British Museum | Not counted | CC BY-NC-SA 4.0 (digest) [17] | Ask | ASK | Share-alike and non-commercial |
| San Diego Museum of Art (Binney) | Pahari and other Indian painting | No terms found [18] | Ask the museum | ASK | |
| Wikimedia Commons | CC0: Kandariya Mahadeva [21], makara [22]; PD-Art: Salt aquatint [23] | Per file | Prefer CC0 and PD-Art; CC BY with credit; CC BY-SA only if the maker accepts share-alike | `artwork`, per file | PD-Art means "faithful reproduction of a public-domain 2D work", with a re-use caution outside the US [20] |
| Google Arts & Culture | Mirrors of museum holdings | Partners keep rights [19] | View only; find the museum's own record | OUT | A zoom is not a licence |
| Living folk artist or cooperative | Pattachitra, Madhubani, Tanjore, Kalamkari, Phad | Written, signed licence or assignment (s.19) [25] | Commission with the F9 brief | `commissioned_art` | Defaults: five years, India only |
| Temple-trust calendar art, Amar Chitra Katha, Pinterest reposts | | Owned [97] | Out | OUT | |
| Raja Ravi Varma plates | PD in India from 1 Jan 1967 (arithmetic), US PD if published before 1931 | s.22 [25][48] | Hand-trace after a plate-level check | `deity_image`, per plate | Later Press designs by other artists |
| The maker's own photograph of her shelf | | Own work | Three-dimensional murtis only | `deity_image`, `cloud: none` | A photograph of a framed calendar print reproduces someone else's artwork: not cleared by being yours |

### T6. `hindu_idiom` block: decision 11 for the style bible (cinematic-quality T2)

```yaml
11_hindu_idiom:   # slots after 10_never_list; refers to decisions 1-10 by name and never edits them (W-38, D-28)
  inherits: [1_palette_per_era, 2_hand_made_material, 3_line_and_edge, 4_typography, 6_reconstruction_marker, 9_title_system, 10_never_list]
  status: "DRAFT until O-36..O-42 are answered; every TODO_maker is the maker's own answer, never a team guess"
  household_keys:                       # the unknowns every field below depends on
    region_state_district: TODO_maker   # O-36
    mother_tongue_and_script: TODO_maker
    prayer_language: TODO_maker
    sampradaya: TODO_maker              # O-37
    kuldevi_or_kuldevata: TODO_maker    # O-38
    ishta_devata: TODO_maker
    shelf_inventory: TODO_maker         # list only; photograph nothing until W-32 allows
    hands_in_hindu_register: TODO_maker # O-40: kolam | alpana | rangoli | embroidery | garlands | diyas | none
    deities_on_a_public_screen: TODO_maker   # O-42: P0 none | P1 symbols | P2 hand-traced plate | P3 own shelf photograph | P4 commissioned painting
    room: TODO_maker                    # O-44
    phone_orientation_she_uses: TODO_maker   # question V7
  d28_rule: "Hindu / Sanatan Dharma only. No Mughal or other Islamic motif, no Christian motif. Shared or ambiguous motifs are flagged and out by default; the maker overrules one line at a time in the log below."
  tradition_primary: TODO_maker         # one eligible row of matrix T1
  tradition_secondary: TODO_maker       # or none
  deity_policy: P1_symbols_only         # default until O-42. AI generated or altered deity: never.
  deity_forms: []                       # one entry per form: {form, sheet_row, her_shelf_image_id, source_route, sign_off}
  motif_whitelist: []                   # only motifs that are hers: her festival, her shelf, her hands
  motif_exclusions_ref: "research/hindu-visual.md exclusion list E1..E26"
  maker_overrules_log: []               # {date, entry, one line of the maker's reason}; nothing else may relax an exclusion
  floor_art_form: TODO_maker            # kolam | muggu | rangoli | alpana | mandana | aipan | jhoti | pookalam | none
  architecture: {order: TODO_maker, elements_allowed: [], elements_flagged_out: [jaali, chhatri, cusped_arch, dome]}
  idiom_line_px_1080: {meaning_bearing_min: 4, decoration_floor: 3, dot_min: 6, hole_min: 4, hatch_stroke_min: 3, hatch_pitch_min: 9, hairlines: banned}   # M-H1; stricter than decision 3, never looser
  appears_in: [title_and_chapter_cards, set_dressing_of_the_one_built_room, floor_art_card_device, torana_or_kalasha_frame_at_module_breaks, deity_symbol_or_plate_if_policy_allows]
  never_in: [real_faces, real_photographs_beyond_their_L1_L2_label, object_clock_transition (W-32), hands_grammar (W-33)]
  coexists_with_2_and_6: "If hands_in_hindu_register is something she made (kolam, alpana, embroidery, garlands), decisions 2, 6 and 11 are one thing: the reconstruction is drawn in that craft's own line, and the idiom adds only subject (a form or motif) and architecture. If not, decision 2 stays her actual material and the idiom dresses cards, titles and set only."
  accent_colour_rule: "A rasa or festival accent lives inside decision 1's era palette and never replaces it (hindu-frameworks track)"
  fonts_and_script: "devotional-sound-script track: OFL Indic families and the shaping fixture"
  respect_rules: "T4 R1..R20; the maker approves each deity drawing as proxy; default OUT on any doubt (D-04)"
  reference_moments: []                 # exactly three, each a shot only she could have (see the worked examples)
  refuses_to_look_like:                 # W-38 asks for this list
    generic_india: [taj_mahal_silhouette, snake_charmer, saffron_drone_shot_of_a_temple, incense_smoke_stock, lens_flare_on_a_diya, curry_display_font, bollywood_poster_framing, tourism_ad_grade]
    colonial_christian_layer: [disc_halo, winged_apsaras, cherubs, candle_for_diya, church_bell_for_ghanta]
    deity_misuse: [generated_deity, mirrored_murti, deity_dissolve, glossy_gold, human_hand_in_hand_with_deity, mughal_arch_or_dome_for_an_india_feel]
    pan_hindu_where_she_is_regional: [festival_she_does_not_keep, deity_form_not_on_her_shelf]
  tests:
    - "swap: replace her household with the other worked example; the block must produce a visibly different film"
    - "T4 R1..R20 on every deity shot; two counts of arms and attributes"
    - "phone fixture: every idiom line at or above idiom_line_px_1080 on the chart before G1"
    - "no entry touches decisions 1-10 except by name"
```

**Worked examples (invented households, to prove the block yields two different films).**

*Household A: the kolam-keeper.* Region: Tamil-speaking south; sampradaya: leans Vaishnava; shelf: a brass lamp and a small bronze Gajalakshmi; hands: she draws a kolam at dawn. Fill: `tradition_primary` floor art (kolam), which is also decision 2 and 6; `tradition_secondary` Tanjore manner for one plate only if O-42 allows (P2 or P4); `architecture` Dravida: a gopuram tilt as the module break, a mandapa only if a wedding photograph exists; `deity_policy` P3 (photograph of the bronze and the lamp, `cloud: none`); `floor_art_form` kolam, cream line on a dark floor at 4 px with 6 px pulli. Reference moments: (1) wet floor, a hand lays rice-flour lines around a dot grid; (2) the day's feet cross it and it is swept, the erasure is the time passing; (3) the lamp lit, a hand shielding the flame. Refuses: kolam from stock vector with 1 px lines, a Bengal alpana under a Tamil lamp, an arch from a Mughal tomb.

*Household B: the wall-painter.* Region: Mithila; sampradaya: Shakta; shelf: a Devi image; hands: she painted the wedding-room wall. Fill: `tradition_primary` Madhubani redrawn coarse (3 px strokes at 9 px pitch, 6 px dots) for cards only; `deity_policy` P1 (fish, lotus, parrot, kalash); `architecture` none (a courtyard, not a temple); `floor_art_form` aripana. Reference moments: (1) a red-and-black line crossing a mud wall; (2) the lamp before the Devi shelf; (3) the wedding room, hands pressing a hand-print. Refuses: a Tamil gopuram, a Tanjore gold panel, a pan-Hindu Diwali she does not keep.

The two blocks share nothing but the rule set and the phone floor; both leave decisions 1 to 10 untouched.

### T7. What agents can build as seekable SVG (Route A) and what needs a hand

| Element | Agent (Route A, `seekTo(t)`) | Needs a human hand | Constraint | Note |
|---|---|---|---|---|
| Kolam, muggu, rangoli, alpana line-draw | Yes: pulli grid, closed stroke around dots, `stroke-dashoffset` against `pathLength` | The maker approves the pattern against her own | Line 4 px (cream on dark), dots 6 px | Method read from [45]; do not link the AGPL toolkit [50] |
| Torana, kalasha, amalaka, lotus, diya, Om, conch, discus, trident, veena, vel, bell | Yes: vector from the sheet | The maker approves every symbol | 4 px strokes | Checked against T3 |
| Shadow-puppet cut-outs | Yes: layered SVG, `data-pivot` per joint (four to twelve), `data-z` order | The maker draws the face and ornament motifs | Holes 4 px or more; a backlit translucent layer | No filters survive VectorCraft |
| Temple silhouettes (shikhara, vimana, gopuram tiers, mandapa colonnade) | Yes: flat vector | Tiers and ornament checked against T2 | Bands 6 px or more | Tilt, never dissolve |
| Kerala-mural colour blocks | Yes: five flat colours | The guna colour assignment is checked | Outline 4 to 6 px | Do not recolour to the era palette |
| Pattachitra border | Yes: parametric pattern | Faces and figures by hand | Border motif 6 px or more | Border stays still |
| Madhubani fill | Partly: coarse hatch generator | Figure fields by hand | Hatch 3 px at 9 px pitch | Different look from the original |
| Kalighat figure | No | Yes: a hand drawing in VectorCraft or on paper | Outline 6 px or more | Wash baked |
| Tanjore panel | Flat version only | Gilding relief and bead glints by hand or baked render | Gem 6 px; highlight baked | No filter-made glint |
| Any deity figure | **Never drawn by an agent** | Hand-traced from a logged plate or hand-drawn by the maker, then proxy approval | R1 to R20 | `deity_source` filled |
| Her own embroidery or hand-made material | A parametric stitch can be generated | Her own hand-made look comes from her material | 4 px stitch line | Decision 2 |

### T8. Rights-log and consult deltas (theatrical-delivery T8 and T10)

- **T8 `type` values to add:** `artwork` (a museum or archive image), `deity_image` (any depiction of a deity, however sourced), `commissioned_art`. **Columns to add:** `tradition_origin` (hindu, shared-flagged, excluded, dharmic-not-hindu, adivasi-ask), `licence_text_saved` (path and date), `plate_screening` (R18 result), `deity_form`, `deity_source`, `commission_assignment_ref`. Sample rows: `AR-001, artwork, Wellcome plate d6dv9m92 (Ganesha with rat, Public Domain Mark), tradition_origin hindu, licence_text_saved 2026-10-19, plate_screening NOT DONE, status VERIFY`; `AR-002, artwork, Kandariya Mahadeva temple photograph, CC0 Ms Sarah Welch, reference only, status GRANTED`; `CA-001, commissioned_art, [form] in the [tradition] manner, assignment worldwide, all media including phone file and archive, term [x], status NS`.
- **T10 consult list, add:** 21. For a painting commissioned for payment and used in a film, who owns the copyright in India under s.17(b) and its proviso, and what must a written licence or assignment state (worldwide, term, all media including a phone file and an archive copy)? 22. In the premiere country, is a faithful museum photograph of a public-domain painting protected, and does a CC0 or PD-Art label clear it? Does a hand redrawing of a CC BY-SA photograph carry a share-alike duty? 23. May the end credits and a phone-file description say "in the manner of Pattachitra" without breaching the GI Act or passing off? 24. Does depicting deities in a devotional animated film carry exposure under religious-feelings offences in India (a lead: BNS s.299, formerly IPC 295A, UNVERIFIED) or in the premiere country, and does a symbols-only policy change it? 25. Does an Indian author's moral right (s.57, from background knowledge, UNVERIFIED) require credit or restrict cropping, recolouring or redrawing of a licensed painting?

### T9. The swastika: the maker's call alone (O-44 informs it)

What the sources say. The Sanskrit word combines *su* and *asti*, "all is well"; Hindus draw it at the threshold of homes, businesses and temples, and at Diwali it may be washed away and redrawn, placed in a rangoli or formed from arranged diyas [88]. The Nazi emblem was the *hakenkreuz*; HAF says early English translations of *Mein Kampf* used "swastika" in its place [88]. A search digest of a HAF-credited explainer describes the Nazi version as tilted 45 degrees, black on a white disc on a red field (digest only) [88], and a digest of a news report says the form generally used in India is right-facing (digest only). Laws in some countries restrict Nazi symbols; I read none, so that is a lead only.

Options: **S0** none (Om, lotus, kalash and diya carry the threshold); **S1** only inside a floor drawing, in kumkum-red, with four dots, upright and right-facing, never black on white or on a red field, never tilted, never on a flag or banner, never as a title element; **S2** as a threshold symbol in her house, only for a room that reads it. Default: S0 for a mixed public room or any room outside India (J); the maker chooses S1 or S2 once O-44 says who is in the room.

### T10. Decision tables keyed on the unknowns

**K1. Region (O-36) to candidate set.** (S where sourced; the rest J.)

| Region | Architecture | Floor art | Painting or craft | Puppetry | Notes |
|---|---|---|---|---|---|
| Tamil Nadu | Dravida: vimana, gopuram, mandapa, tank [52][54] | Kolam; Margazhi [45] | Tanjore [33] | not researched | Sri Vaishnava Andal tradition [46] |
| Andhra, Telangana | Vijayanagara-era Dravida; Lepakshi is the cited reference for the puppet palette [44] (architecture order J) | Muggu [46] | Srikalahasti Kalamkari [41]; Cheriyal (Telangana) [39] | Tholu Bommalata [42] | Machilipatnam out [41] |
| Karnataka | Vesara (Hoysala), Dravida [52] | Rangoli [46] | Mysore [34] | Togalu Gombeyaata (costume flag) [43][44] | Kalyani tanks [59] |
| Kerala | Own regional type (J) | Pookalam [46] | Kerala murals [32] | Tolpavakoothu (UNVERIFIED) | Mattancherry flag |
| Maharashtra | Not researched | Rangoli [46] | Not researched | not researched | Vitthal [61]; Ashtavinayak [64]; Warli is Adivasi (ask) |
| Gujarat | Nagara (Chaulukya-era toranas), stepwells [56][59] | Sathiyo, rangoli [46] | Pushtimarg pichwai if Pushtimarg [38] | not researched | Check Islamic-era stepwells [59] |
| Rajasthan | Nagara; chhatri and jharokha flagged [57] | Mandana [46] | Phad [40]; pichwai [38]; Rajput court (flag) [37] | not researched | Phad is Joshi craft |
| Bihar (Mithila) | Nagara (north) | Aripana (J) | Madhubani [31] | | |
| West Bengal | Own regional type (J) | Alpana [47] | Kalighat [29]; Bengal patachitra GI 2018 [30] | | Kali, Durga Puja |
| Odisha | Nagara, Kalinga rekha deul [53] | Jhoti, chita [46] | Pattachitra [30] | | Jagannath [70] |
| Uttar Pradesh, Madhya Pradesh, Uttarakhand, Himachal | Nagara [52][53] | Chowkpurana, aipan, mandana [46] | Pahari/Kangra (flag) [35] | | |
| Punjab, Northeast, Goa | Not researched | | | | Ask; dharmic and Adivasi overlays |

**K2. Sampradaya (O-37) to marks and image rule.** Vaishnava: vertical U mark [74]; Venkateswara, Krishna, Rama, Vitthal, Jagannath forms; pichwai only for Pushtimarg [38]. Shaiva: tripundra [74], linga primary [75], Nandi, Shiva family. Shakta: red dot among three lines [74]; Durga, Kali, Devi Mahatmya forms. Ganapatya: red sandal [74]. Smarta (five-deity household): not sourced, ask. Rule: never mix one sect's mark or image into another's home; a Shaiva home gets no pichwai Shrinathji [38].

**K3. Shelf (O-38) to the sheet.** Each deity on her shelf gets one row of T3 and one `deity_forms` entry. Ground truth is her own shelf image (a photograph of a three-dimensional murti or lamp, `cloud: none`); if only a framed print is there, it is not photographed (copyright of the print, T5). The agamic default fills the gaps; disagreements go to the maker. A kuldevi without a standard form is shown only as a symbol or not at all.

**K4. Hands (O-40) to decisions 2, 6 and 11.** Kolam, muggu, rangoli, alpana, aipan, mandana, jhoti: the reconstruction is drawn in flour-line on a dark floor (cream on indigo held at 3 px and above in the fixture). Embroidery or thread: a 4 px stitch line. Garlands or pookalam: dot-built flowers at 6 px. Diyas or lamp polishing: small raised relief. She painted: her own tradition is primary (Madhubani and the like, redrawn at the floor). None: decision 2 stands on her actual material; the idiom dresses cards and set only.

**K5. Deities on a public screen (O-42).** Policy tiers P0 to P4 (named P so they are not confused with the T-numbered templates). P0 none: sound, symbols and no figure. P1 symbols only: lamp, kalash, lotus, conch, Om, linga, padukas, yantra, tulasi. P2 hand-traced public-domain plate (logged, screened, proxy-approved). P3 her own shelf photograph of a three-dimensional murti. P4 a commissioned painting under written licence. AI: never. Default P1 until she is answered for (J). Note the 1992 precedent that some devotees object to animated gods at all [91].

**K6. Room (O-44) to the swastika, the captions and the explaining.** India, mostly Hindu: S1 or S2 by the maker; deity terms unexplained. Mixed public room abroad: S0; one card names what a lamp, a kolam and a torana are, once, if the maker wants it. A room with Hindu elders: R1 to R20 apply fully and the maker may add stricter rules.

### T11. A worked shot brief from the sheet (illustrative, not for production)

*Brief: "Gajalakshmi, Tanjore manner."* Form: Lakshmi seated on a lotus, with two elephants behind her pouring water from pots over her [62][65]. Hands: pick one from her shelf image: the agamic four (long-stalk lotus, bilva fruit, amrita pot, conch) [62] or the popular print (lotus in one or two hands, one hand pouring wealth) [65]; if she has none, ask. Colour: golden, red dress with gold thread, smaller than any Vishnu in the frame [65]. Manner (Tanjore [33]): central figure largest under an arch or flame arch, rounded face, almond eyes, flat bright colours, smooth streamlined body; omit the "angel-like seraphs"; gold as a flat colour with a baked highlight, no filter (R13); glass-bead gems as dots of 6 px or more; outlines 4 px or more. Motion: a still with one slow push of at most 4%, inside decision 5's 8% range; no transition on the figure (R5); a lit lamp before the image, a hand may shield it (R15). Source (R17): agent-drawn vector from the sheet and hand-finished by the maker, or a commissioned Tanjore panel under written licence; no public-domain Tanjore plate was found in this sprint. Checks: R1 to R20, two counts of arms and attributes, phone check on the fixture chart, maker approval as proxy, Fable flag.

### Acceptance tests from the Fable brief (1.4), self-applied

- **Matrix.** Every score has a one-line reason; no tradition is scored on phone legibility without the fixture (the Phone column reads the F3 table); the "collapse once O-36 and O-37 are answered" rule is stated. Gap: effort is judgment, not measured hours.
- **Checklist.** A shot of "Lakshmi, Gajalakshmi form, Tanjore manner" can be briefed from T3 and T11 without a search. Every "don't" names its source or says (J).
- **Exclusion list.** No entry says "probably fine"; shared motifs are out by default; each carries an origin note and a question.
- **Block.** Two invented households give two films; decisions 1 to 10 are touched only by name; coexistence with decision 2 and 6 is stated. Gap: `rasa_accent_rule` and fonts are the other tracks'.

---

## Exclusions and ambiguous cases (under the maker's Hindu-only rule)

Rule applied (D-28, review 04 section 0.1): name the origin honestly, flag, default **out**, put the exception to the maker in one line, never present a shared motif as Hindu to get it past the rule, never include it because "she would not mind". The rule governs motifs, not people: an artist's own community is not a motif (question V6). Labels: (S) from a page I read, (J) background knowledge or inference. "Hers beats generic": if a flagged item is on her actual sari, in her actual photograph or in her actual temple, it is hers, and the maker decides that one line at a time.

| ID | Motif | Origin note (one line) | Default | Question if an exception is worth asking |
|---|---|---|---|---|
| E1 | Jaali (pierced screen) | Shared: pre-Islamic cave and temple screens persisted in Hindu and Jain temples, but the geometric and calligraphic development is Delhi Sultanate and Mughal (Alai Darwaza 1305) (S) [58] | Out | Is there a jaali in a real place in her life? |
| E2 | Cusped or multifoil arch | Widespread in Indo-Islamic building; the temple toranas of Chaulukya Gujarat are scalloped gateways (J), so the form is shared and the arch alone proves nothing [56] | Out | Is there a temple toran in her real temple? |
| E3 | Onion or bulbous dome | Persianate form carried by Mughal building (J); the amalaka disc and kalasha urn on a Nagara tower are not domes (S) [53] | Out | None |
| E4 | Chhatri | Rajasthani origin yet "found particularly within Mughal architecture"; Hindu cenotaphs exist (Alwar's Musi Maharani ki Chhatri with Ramayana and Mahabharata murals; Orchha) (S) [57] | Out as set dressing | Is a named Hindu cenotaph part of her place? |
| E5 | Taj Mahal and Mughal monuments, minarets, arabesque borders, crescent | Islamic; also on the generic-India list | Out | None |
| E6 | Indo-Saracenic palaces, stations and civic buildings | Colonial revival mixing dome, chhatri and arch (J) | Out | None |
| E7 | Hawa Mahal façade | Built under a Hindu ruler in 1799 (J) but a Rajput screen-and-jharokha façade with Mughal ancestry (J) | Out | Is it hers? |
| E8 | Stepwells under Islamic patronage | "Construction hit its peak during Muslim rule from the 11th to 16th century" (S) [59]; Rani ki vav and Chand Baori attribution needs a second source | Out until each is checked | Which stepwell, and what is the source for its builder? |
| E9 | Mughal-style court painting, its borders and portraiture | Islamic court art | Out | None |
| E10 | Pahari/Kangra, and Bundi, Kota, eastern Marwar Rajput painting | Kangra began with "Kashmiri painters trained in the Mughal painting style"; Bundi and Kota were "influenced directly by Mughal painting" (S) [35][37]; subject matter is Vaishnava | Out | Would you accept Basohli or the pre-Mughal Chaurapanchasika-type Mewar idiom, which the sources describe as earlier and bolder [36][37]? |
| E11 | Machilipatnam kalamkari, Persian floral interlace | "Persian-influenced motifs"; made under Golconda and Mughal patronage (S) [41] | Out | None (Srikalahasti stays) |
| E12 | Togalu puppet men's beards and boots; other Islamic-influenced puppet costume | Karnataka puppets "blend influences from the Halebid Hoysaleshwara temple and Islamic culture" (S) [44] | Out; use Tholu forms | Replace with Andhra figures? |
| E13 | Winged attendants in Tanjore ("angel-like seraphs") and winged apsaras | A Tanjore convention [33]; apsaras are not winged in the Hindu tradition (J) | Out | None |
| E14 | Kerala mural sites that are palaces or churches | The style is Hindu; the site list includes Mattancherry Palace and "several churches" (S) [32] | Use the style, not the set | None |
| E15 | Colonial-Christian layer in popular prints: cherubs, disc halos, candles for diyas, church bells for ghantas | The brief's lead; UNVERIFIED, nothing I read confirmed it; the Ravi Varma Press passed to a German printer in 1901 [48] | Check plate by plate; out if present | None |
| E16 | Paisley and buta (boteh) | Persian-origin textile motif (J); common on saris and shawls | Out | Is it on her actual sari or shawl? |
| E17 | Mehndi (henna) | Worn at Hindu weddings; its origin is debated and shared (J) | Flag | Is it in her wedding photographs? |
| E18 | Ayyappa's Vavar pairing and mosque | In the pilgrim story and at Sabarimala's foothills a mosque for Vavar stands beside the Kadutha shrine (S) [72] | Out of frame | None |
| E19 | Persian, Urdu and Arabic calligraphy, qawwali visual cues | Islamic | Out | None |
| E20 | Christian: crosses, disc halos, angels, cherubs, candles, church bells, stained-glass arches | Christian | Out | None |
| E21 | Dharmic, not Hindu: Jain miniature painting, Buddhist Ajanta and Sanchi, Sikh Punjabi and Gurbani imagery | Close cousins outside the maker's definition (review 04, 0.1) | Out; ask | Does she keep any of these? |
| E22 | Adivasi art: Warli, Gond, Bhil or Pithora, Saura | Often sold as "Indian folk art" with their own deities (J); Sabnani's Bhil film is this [100] | Out; ask | Is it hers? |
| E23 | Lotus | Shared dharmic symbol, but Lakshmi's and Vishnu's own seat (S) [65] | In, with a Hindu context | None |
| E24 | Swastika | Sacred and at every Hindu threshold [88]; read as something else by strangers | The maker's call, T9 | O-44 |
| E25 | Saffron flag, party colours, slogans, maps, temple politics | Not a Hindu motif but a political one in a mixed room (review 04, 0.1) | Out | Decide like a hard chapter |
| E26 | Islamic-geometry star patterns (girih) or arabesque in modern rangoli and cut-work | Islamic geometry (J) | Out | None |

---

## Tools, sources, services and costs (as of 2026-10-19)

| Item | Status today | Cost | Note |
|---|---|---|---|
| Met Collection API | v1 search retired 2026-10-01, v1.1 search works (`/public/collection/v1.1/search`) [5] | Free | Object records still on v1; images page blocked (429) |
| Smithsonian Open Access API | Works with `DEMO_KEY` (rate-limited) [8]; GitHub repository archived 21 May 2026 [7] | Free; register a key (UNVERIFIED process) | The public website blocked us (403) |
| Cleveland open-access API | Works [3] | Free | |
| Wellcome Catalogue API | Works; licence ids per item [15] | Free | |
| AIC API | Docs read [9]; website blocked (403) | Free | Images: "up to you" |
| Wikimedia Commons API | Rate-limited after two queries ("too many requests") | Free | Use file-page reads, a descriptive user agent and slow, spaced queries |
| archive.org | Rao 1914 full text readable | Free | The three volumes used are listed in the sources |
| ffmpeg 6.1.1, ImageMagick 6.9.12, rsvg-convert | Used for the fixture in the cloud container | Free | Windows builds UNVERIFIED (W-28) |
| Commissioned painting (marketplace listings) | INR 15,000 (12 by 18 in Pattachitra) to INR 26,000 (24 by 40 in); INR 21,600 (15 by 12 in Tanjore, 22k); Madhubani sets from about INR 4,200; Tanjore 42 by 54 in framed US$5,020 [106][107] | Plan INR 15,000 to 50,000 or more (J) | Pages blocked (429); digests only; get quotes |
| Museum commercial image licences | V&A and British Museum on request [16][17]; Harvard "no fee" but a licence request (digest) [12] | Unknown | Ask only for an image that cannot be replaced by a CC0 one |
| Consult hour (TD-8) | Five questions added (T8) | Already budgeted (O-27) | |
| Blocked to our tools today | si.edu, artic.edu, britishmuseum.org, smarthistory.org, the Met images page, MeMeraki | | Re-read from the maker's own browser before any image is chosen |

---

## Changes to existing playbooks (file, section, what changes)

| File | Section | What changes |
|---|---|---|
| `playbooks/cinematic-quality.md` | T2 Style bible, ten-decision table and YAML | Add `11_hindu_idiom` exactly as in T6 and a row 11 in the one-line table; decisions 1 to 10 untouched. In `3_line_and_edge` add `phone_min_stroke_px_1080: 4` for meaning-bearing lines and a floor of 3, and a "recompressed twice" variant of the three-background test (M-H1) |
| `playbooks/cinematic-quality.md` | T1 item PR2 "Thin lines" (and the "What good looks like" note near line 190, Pitfall 8) | PR2 tests the access-copy encode only (a 1 px line keeps 0.98 there, matching the existing M-C6). Add PR2b: after the two chat-app proxies, lines of 3 px keep at least 0.6, lines of 4 px at least 0.8; dots 6 px; holes 4 px; hatch stroke 3 px at 9 px pitch; no 1 px. The "strokes are at least 2 px" reasoning is correct for a room and wrong for a phone |
| `playbooks/cinematic-quality.md` | T5 Banned cheap tells | Add the generic-India tells (Taj silhouette, snake charmer, saffron drone shot of a temple, incense smoke stock, lens flare on a diya, a "curry" display font, Bollywood poster framing, tourism grade), the colonial-Christian layer (disc halo, winged apsaras, cherubs, candle for diya, church bell for ghanta), and the deity tells (generated deity, mirrored murti, dissolve on a deity, glossy gold, a human hand in hand with a deity). W-38's test applies: if the shot would work for another family it is out |
| `playbooks/cinematic-quality.md` | T6 Projection-truth checklist | Add a phone-truth sub-list: landscape full screen (1.0) and upright inline (0.5625) views; the fixture chart through the two chat proxies |
| `playbooks/cinematic-quality.md` | T9 AI-tells catalogue | Add rows 24 to 28: deity attribute or arm-count error (BANNED; UNVERIFIED as an AI-specific measurement); wrong skin colour for a form; sexualised or aggressive deity; fabricated ritual; a human beside a deity at the same level. All BANNED in the public cut |
| `playbooks/cinematic-quality.md` | Exercise 9 "Thin lines and small type" | Add a phone pass with `phone_chart.svg` through the two proxies and read the table in F3 |
| `playbooks/cinematic-quality.md` | Decisions table, row 6 reconstruction marker | Where her hands made floor art, embroidery or garlands, the marker is that craft's line (K4); where the idiom is separate, it dresses cards, titles and set only |
| `playbooks/cinematic-quality.md`, `playbooks/animated.md` | Best references | Add the exemplars of F2 with dates and the lessons in "Exemplars and what they teach us" |
| `playbooks/animated.md` | Decision 1 (How invented scenes look), option (a) | Name floor-art line, shadow-puppet cut-out and scroll-panel as candidate hand-made idioms if hers; W-38 stays in charge |
| `playbooks/animated.md` | Exercise 7 "A title card on paper" | Becomes a floor-art card: one kolam, alpana or rangoli line-draw on a dark ground at 4 px with 6 px dots, timed |
| `playbooks/ai-imagery.md` | Step 9 Route A and Routes B to D | Remove the voxel tools (already on review 04's list); add: no generative route for a deity figure; a deity is hand-drawn, hand-traced from a logged public-domain plate, a shelf photograph or a commissioned painting; Route B edits, Route C adapters and Route D LoRAs are never used on a deity |
| `playbooks/ai-imagery.md` | Step 10 label ladder; `steps.csv` | `deity_image` rows carry L0 or L1 (shelf photograph), L2 only for non-generative scaling, L3 for a traced plate; never L4b or L5; add `deity_form` and `deity_source` columns |
| `playbooks/ai-imagery.md` | Decision 3 (non-commercial weights) and Pitfalls | Note that deity line-art and vector symbols need no model at all; add the AI-deity pitfall with [79][83][84] |
| `playbooks/theatrical-delivery.md` | T8 rights log | New types `artwork`, `deity_image`, `commissioned_art`; new columns and sample rows from T8 above; the written-assignment rule for commissioned work |
| `playbooks/theatrical-delivery.md` | T10 consult list | Add questions 21 to 25 (T8 above) |
| `playbooks/theatrical-delivery.md` | Step 11 (rights tiers) | State that a museum licence is per record and that CC BY-NC and "non-commercial" terms are "ask", not "yes", for a public screening |
| `playbooks/agent-pipeline.md` | Templates, shot brief YAML; G2 review pack | Add `motif_check` (hindu, flagged, excluded), `deity_form`, `deity_source`, `respect_check` (R1 to R20) and `phone_stroke_ok`; Fable reads every `flagged` brief; the G2 pack includes the arm-and-attribute count |
| `playbooks/agent-pipeline.md` | Route A section | Floor-art line-draw and shadow-puppet hinges as Route A examples (`pathLength`, `data-pivot`) |
| `playbooks/craft-visual.md` | "SVG hooks that do not survive" | Note that VectorCraft drops filters, so filter-made gold and glow are lost, which R13 wants |
| `DECISIONS.md` (orchestrator) | New rows | Default `deity_policy` P1 (symbols only) until O-42; phone stroke floor 4 px (3 px decoration); default landscape-first design; the questions V1 to V8 below as O-rows; add the Table 4 stale rows already listed in review 04 |

---

## Open questions for the maker

All can be answered from the maker's own knowledge or by looking at the house, without asking anyone (D-03) and without a note that would tip her off (D-02). The first six are the existing O-36 to O-44 seen from this track; V1 to V8 are new (numbers provisional, for the orchestrator).

1. **O-36 region, language, script.** Gates every row of K1 and the architecture order.
2. **O-37 sampradaya.** Gates marks, the pichwai and which form of Vishnu or Shiva appears.
3. **O-38 kuldevi, ishta devata, temple, shelf.** One row of T3 per form on the shelf. Describe the shelf in words first. Photograph a three-dimensional murti or lamp only on an unsynced phone, never a framed print, never in a temple.
4. **O-40 her hands.** Kolam, rangoli, alpana, mandana, embroidery, garlands, diyas, painting? Decides whether decisions 2, 6 and 11 are one thing.
5. **O-42 deities on a public screen.** Policy tiers P0 to P4 (K5). Some devout households and some devotees object to animated gods at all [91]. Default until answered: P1, symbols only.
6. **O-44 the room.** Decides the swastika (T9) and how much a card explains.
7. **V1 Her own images.** What printed or painted deity images hang or stand in her home today? They are the ground truth, and a calendar print is someone's copyrighted artwork (T5).
8. **V2 Flagged items that are hers.** Are any E-entries on her real things: paisley on her sari, mehndi in her wedding photographs, an arch in her family temple, a stepwell near her village? Each is decided one line at a time.
9. **V3 Pahari or Rajput.** If the maker loves Pahari or Rajput court painting, is the Basohli or Mewar pre-Mughal idiom acceptable instead (E10)?
10. **V4 The scroll.** Would the film be told as a life in panels (a Phad or Cheriyal-style scroll with a pointer and a lamp)? It is the strongest structural fit found (F1), but it needs a Rajasthani or Telangana link or a commissioned panel.
11. **V5 Commissioning.** May a gallery, cooperative or artist be told only "a film project to be shown publicly in 2027, no names, written film licence"? That is a D-07-type boundary and the maker's call (F9).
12. **V6 Artists and the rule.** D-28 governs motifs. May a practising Madhubani or Pattachitra artist of any community be commissioned for a Hindu subject? Asked only because commissioning pages list artists of different communities.
13. **V7 Her phone.** Does she hold it sideways to watch, or watch inline in a chat? That sets whether the film is designed for landscape full screen (the default here) or for the 0.56-scaled chat view (F3). Extends O-43.
14. **V8 Plates.** Is the maker willing to personally screen each public-domain deity plate (R18) and approve each hand-traced drawing as proxy (R17), given the hours that costs?

---

## Sources

Format: [n] title — URL — date read or queried — one-line note. "Read" means I opened the page and used its text (the fetch tool returns a summary plus short quoted fragments, so quotations in these notes are fragments). "Queried" means an API response I read. "Digest only" means I saw the URL in a search result and could not open the page, or did not; nothing marked so is quoted as if read. Wikipedia pages are secondary and were read only to the point the fetch tool cut them (about 100,000 characters); I used them for orientation and attached a primary or a caution wherever a claim carries weight.

**Rights and law**

[1] Cleveland Museum of Art, Open Access — https://www.clevelandart.org/open-access — 2026-10-19 — CC0 images and data; exclusions; launched January 2019 (read).
[2] Cleveland, "Raja Sansar Chand of Kangra and courtiers", c. 1783 — https://clevelandart.org/art/1986.63 — 2026-10-19 — "Public Domain ... without asking permission" (read).
[3] Cleveland Open Access API — https://openaccess-api.clevelandart.org/api/artworks/?q=Pahari&cc0=1&limit=1 — 2026-10-19 — keyword counts with cc0=1 (queried).
[4] Metropolitan Museum, openaccess data README — https://github.com/metmuseum/openaccess — 2026-10-19 — data CC0, more than 470,000 artworks, images not included (read).
[5] Metropolitan Museum Collection API — https://collectionapi.metmuseum.org/public/collection/v1.1/search?isPublicDomain=true&q=gopuram&limit=20&offset=0 and https://collectionapi.metmuseum.org/public/collection/v1/objects/287277 — 2026-10-19 — v1 search retired 2026-10-01; Tripe 1858 gopuram records flagged public domain (queried).
[6] Metropolitan Museum, Image and Data Resources — https://www.metmuseum.org/policies/image-resources — 2026-10-19 — HTTP 429 to the fetch tool and curl; terms from a search digest only (UNVERIFIED).
[7] Smithsonian Open Access repository — https://github.com/Smithsonian/OpenAccess — 2026-10-19 — CC0-1.0, over 11 million records, repository archived 21 May 2026 (read).
[8] Smithsonian Open Access API, record `edanmdm:fsg_S2018.1.3` — https://api.si.edu/openaccess/api/v1.0/content/edanmdm:fsg_S2018.1.3 (public DEMO_KEY, rate-limited) — 2026-10-19 — NMAA "Krishna Vishvarupa", "Restrictions & Rights: CC0"; also the image-record counts (queried).
[9] Art Institute of Chicago API documentation — https://api.artic.edu/docs/ — 2026-10-19 — data CC0; "This API does not contain image files"; "It is up to you ..." (first 100,000 of 441,115 characters read).
[10] LACMA, Terms of Use — https://www.lacma.org/about/contact-us/terms-use — 2026-10-19 — public-domain images "for use without restriction", credit and URL; protected content personal non-commercial (read).
[11] Rijksmuseum, data and image policy — https://data.rijksmuseum.nl/policy — 2026-10-19 — Public Domain or CC0, CC BY 4.0, credit requested (read).
[12] Harvard Art Museums, Image Resources — https://harvardartmuseums.org/image-resources — 2026-10-19 — "personal, noncommercial use" (read).
[13] Philadelphia Museum of Art, Legal — https://philamuseum.org/about/legal — 2026-10-19 — images "generally of artworks in the public domain"; no licence name (read).
[14] Wellcome Collection, "Lakshmi lustrated by two elephants" — https://wellcomecollection.org/works/phr7cv3d — 2026-10-19 — CC BY-NC 4.0, reference 26778i (read).
[15] Wellcome Collection Catalogue API, query "Kalighat" — https://api.wellcomecollection.org/catalogue/v2/works?query=Kalighat&pageSize=100&include=items — 2026-10-19 — 184 results; licence tally 96 PDM, 4 CC BY, 3 CC BY-NC, 81 without images (queried).
[16] V&A, website terms and conditions — https://www.vam.ac.uk/info/va-websites-terms-conditions/ — 2026-10-19 — non-commercial free use; commercial through image licensing (read).
[17] British Museum, copyright and permissions — https://www.britishmuseum.org/terms-use/copyright-and-permissions — 2026-10-19 — HTTP 403; CC BY-NC-SA 4.0 from search digests of image pages (UNVERIFIED).
[18] San Diego Museum of Art, collection — https://www.sdmart.org/art/collection/ — 2026-10-19 — no image terms stated (read).
[19] Google Arts & Culture partner FAQ — https://support.google.com/culturalinstitute/partners/answer/6002688?hl=en — 2026-10-19 — digest only: partners keep rights.
[20] Wikimedia Commons, When to use the PD-Art tag — https://commons.wikimedia.org/wiki/Commons:When_to_use_the_PD-Art_tag — 2026-10-19 — Bridgeman v. Corel, "applies in the United States only", re-use caution (read).
[21] Commons file, Kandariya Mahadeva temple (CC0) — https://commons.wikimedia.org/wiki/File:0121821_Kandariya_Mahadeva_temple,_Khajurajo_001.jpg — 2026-10-19 — CC0 1.0, Ms Sarah Welch (read).
[22] Commons file, Hoysaleswara makara (CC0) — https://commons.wikimedia.org/wiki/File:1150_CE_Hoysaleswara_temple_Halebidu_Karnataka,_Makara_mythical_animal.jpg — 2026-10-19 — CC0 1.0, Ms Sarah Welch (read).
[23] Commons file, Brihadisvara Temple by Henry Salt — https://commons.wikimedia.org/wiki/File:Brihadisvara_Temple,_Thanjavur_by_Henry_Salt.jpg — 2026-10-19 — PD-Art, 1809 aquatint, British Library (read).
[24] UK Intellectual Property Office, Copyright notice: digital images, photographs and the internet — https://www.gov.uk/government/publications/copyright-notice-digital-images-photographs-and-the-internet/copyright-notice-digital-images-photographs-and-the-internet — 2026-10-19 — "Updated 4 January 2021"; "seems unlikely" (read).
[25] Copyright Act, 1957, s.17 and the Act — https://indiankanoon.org/doc/1404402/ and https://indiankanoon.org/doc/1136195/ — 2026-10-19 — s.17(b) and proviso, s.19, s.22; the second page shows the 7 June 2012 text; currency UNVERIFIED (read).
[26] Copyright Act, 1957, consolidated copy at the Copyright Office — https://copyright.gov.in/Documents/Copyright_Act_1957.pdf — 2026-10-18 — read for `research/sources/theatrical-delivery-round2-excerpts-2026-10-18.txt` item 4; gives s.17(b) in the same words; PDF metadata 2018.
[27] Geographical Indications of Goods Act 1999, s.22 — https://www.advocatekhoj.com/library/bareacts/geographicalindicationsofgoods/22.php — 2026-10-19 — infringement limbs; text has typos (read).
[28] Eastern Book Company v. D.B. Modak — https://indiankanoon.org/doc/1062099/ — 2026-10-19 — digest only: originality standard; no case on photographs of public-domain paintings found.

**Traditions**

[29] Wikipedia, Kalighat painting — https://en.wikipedia.org/wiki/Kalighat_painting — 2026-10-19 — read (115,847 characters; first 100,000).
[30] Wikipedia, Pattachitra — https://en.wikipedia.org/wiki/Pattachitra — 2026-10-19 — GI dates, conventions (read, truncated).
[31] Wikipedia, Madhubani art — https://en.wikipedia.org/wiki/Madhubani_art — 2026-10-19 — styles, kohbar (read).
[32] Wikipedia, Kerala mural painting — https://en.wikipedia.org/wiki/Kerala_mural_painting — 2026-10-19 — panchavarana, guna colours, sites (read).
[33] Wikipedia, Tanjore painting — https://en.wikipedia.org/wiki/Tanjore_painting — 2026-10-19 — gesso, gold, seraphs, GI 2007 to 2008 (read).
[34] Wikipedia, Mysore painting — https://en.wikipedia.org/wiki/Mysore_painting — 2026-10-19 — single-source article (read).
[35] Wikipedia, Kangra painting — https://en.wikipedia.org/wiki/Kangra_painting — 2026-10-19 — Mughal-trained origin, Vaishnava subject (read).
[36] Wikipedia, Basohli painting — https://en.wikipedia.org/wiki/Basohli_painting — 2026-10-19 — blazing colours, Vaishnava (read).
[37] Wikipedia, Rajput painting — https://en.wikipedia.org/wiki/Rajput_painting — 2026-10-19 — schools, Mughal influence (read, truncated).
[38] Wikipedia, Pichwai — https://en.wikipedia.org/wiki/Pichwai — 2026-10-19 — Pushtimarg, Shrinathji (read).
[39] Wikipedia, Cheriyal scroll painting — https://en.wikipedia.org/wiki/Cheriyal_scroll_painting — 2026-10-19 — format, palette, GI 2008 (read).
[40] Wikipedia, Phad painting — https://en.wikipedia.org/wiki/Phad_painting — 2026-10-19 — Joshi, Bhopa, Pabuji (read).
[41] Wikipedia, Kalamkari — https://en.wikipedia.org/wiki/Kalamkari — 2026-10-19 — Srikalahasti versus Machilipatnam, GI; needs-citations tag (read).
[42] Wikipedia, Tholu Bommalata — https://en.wikipedia.org/wiki/Tholu_Bommalata — 2026-10-19 — hides, joints, repertoire (read).
[43] Wikipedia, Togalu Gombeyaata — https://en.wikipedia.org/wiki/Togalu_Gombeyaata — 2026-10-19 — leather, lamp, invocation (read).
[44] Sarmaya, Tholu Bommalata guide — https://sarmaya.in/guides/tholu-bommalata/ — 2026-10-19 — sizes, perforations, four to twelve joints, Lepakshi and Islamic influences (read).
[45] Wikipedia, Kolam — https://en.wikipedia.org/wiki/Kolam — 2026-10-19 — pulli, sikku, Margazhi, mathematics (read; several claims tagged "citation needed").
[46] Wikipedia, Rangoli — https://en.wikipedia.org/wiki/Rangoli — 2026-10-19 — regional names and materials (read).
[47] Wikipedia, Alpona — https://en.wikipedia.org/wiki/Alpona — 2026-10-19 — freehand, motifs (read).
[48] Wikipedia, Raja Ravi Varma — https://en.wikipedia.org/wiki/Raja_Ravi_Varma — 2026-10-19 — dates, press, oleographs, Schleicher (read).
[49] Sahapedia, "Pattachitra: Tale of Father and Son" — https://www.sahapedia.org/pattachitra-tale-of-father-and-son — 2026-10-19 — border and frontal composition; no date shown; author M. D. Muthukumaraswamy (read).
[50] nhtran93/kolam (R package) — https://github.com/nhtran93/kolam — 2026-10-19 — gesture codes, pulli and loops; AGPL-3.0 (read).
[51] Search digests for GI years and typical subjects — https://vajiramandravi.com/upsc-exam/tanjore-painting/ ; https://vajiramandravi.com/upsc-exam/kalamkari-painting/ ; https://anantamias.com/madhubani-painting/ — 2026-10-19 — digest only; exam-preparation and commercial pages, weak evidence.

**Architecture**

[52] Wikipedia, Hindu temple architecture — https://en.wikipedia.org/wiki/Hindu_temple_architecture — 2026-10-19 — Nagara, Dravida, Vesara (read; first 100,000 of 284,742 characters).
[53] Wikipedia, Shikhara — https://en.wikipedia.org/wiki/Shikhara — 2026-10-19 — latina, sekhari, bhumija; amalaka and kalasha (read).
[54] Wikipedia, Gopuram — https://en.wikipedia.org/wiki/Gopuram — 2026-10-19 — tiers, painted plaster, development (read).
[55] Wikipedia, Mandapa — https://en.wikipedia.org/wiki/Mandapa — 2026-10-19 — types and axis (read).
[56] Wikipedia, Torana — https://en.wikipedia.org/wiki/Torana — 2026-10-19 — Hindu, Buddhist, Jain; Chaulukya; mango-leaf torana (read).
[57] Wikipedia, Chhatri — https://en.wikipedia.org/wiki/Chhatri — 2026-10-19 — origin and Mughal use; unsourced claims noted (read).
[58] Wikipedia, Jali — https://en.wikipedia.org/wiki/Jali — 2026-10-19 — shared tradition (read).
[59] Wikipedia, Stepwell — https://en.wikipedia.org/wiki/Stepwell — 2026-10-19 — names, dating, Islamic-era peak (read).
[60] Smarthistory pages — https://smarthistory.org/lakshmana-temple/ ; https://smarthistory.org/temple-tanjavur/ ; https://smarthistory.org/meenakshi-madurai/ — 2026-10-19 — HTTP 403; search digests only.

**Iconography**

[61] T. A. Gopinatha Rao, Elements of Hindu Iconography, Vol. I Part I (Madras, 1914) — https://archive.org/details/india.history.resource.94142 (text at https://archive.org/download/india.history.resource.94142/94142_djvu.txt) — 2026-10-19 — Ganapati, Vishnu forms, the 24 images, Rama's group, Venkatesa, Vithoba, Jagannatha (read; a 1914 colonial-era scholar, some historical claims contested and not repeated).
[62] Rao, Vol. I Part II (1914) — https://archive.org/details/india.history.resource.94143 — 2026-10-19 — Durga, Lakshmi, Annapurna, Saraswati (read).
[63] Rao, Vol. II Part II (1916) — https://archive.org/details/xHNQ_elements-of-hindu-iconography-vol-2-part-2-t.-a.-gopinatha-rao — 2026-10-19 — Subrahmanya, Sasta (the archive item's metadata shows a CC0 licence field for the upload; the text is a 1916 publication) (read in part).
[64] Wikipedia, Ganesha — https://en.wikipedia.org/wiki/Ganesha — 2026-10-19 (read, truncated).
[65] Wikipedia, Lakshmi — https://en.wikipedia.org/wiki/Lakshmi — 2026-10-19 (read, truncated; regional section not seen).
[66] Wikipedia, Saraswati — https://en.wikipedia.org/wiki/Saraswati — 2026-10-19 (read, truncated).
[67] Wikipedia, Durga — https://en.wikipedia.org/wiki/Durga — 2026-10-19 (read, truncated).
[68] Wikipedia, Kali — https://en.wikipedia.org/wiki/Kali — 2026-10-19 (read, truncated).
[69] Wikipedia, Hanuman — https://en.wikipedia.org/wiki/Hanuman — 2026-10-19 — iconography section cut off; only attribute and Panchamukha lines seen (read, truncated).
[70] Wikipedia, Jagannath — https://en.wikipedia.org/wiki/Jagannath — 2026-10-19 (read, truncated).
[71] Wikipedia, Venkateswara — https://en.wikipedia.org/wiki/Venkateswara — 2026-10-19 (read, truncated).
[72] Wikipedia, Ayyappan — https://en.wikipedia.org/wiki/Ayyappan — 2026-10-19 (read).
[73] Wikipedia, Kartikeya — https://en.wikipedia.org/wiki/Kartikeya — 2026-10-19 (read, truncated).
[74] Wikipedia, Tilaka — https://en.wikipedia.org/wiki/Tilaka — 2026-10-19 — Tenkalai and Vadakalai not covered (read).
[75] Wikipedia, Shiva — https://en.wikipedia.org/wiki/Shiva — 2026-10-19 (read, truncated).
[76] Wikipedia, Vishnu — https://en.wikipedia.org/wiki/Vishnu — 2026-10-19 — the Iconography section was cut off (read, truncated).
[77] Wikipedia, Krishna — https://en.wikipedia.org/wiki/Krishna — 2026-10-19 (read, truncated).
[78] Wikipedia, Rama — https://en.wikipedia.org/wiki/Rama — 2026-10-19 — Sita placed on the right of Rama; Rao differs (read, truncated).

**AI, respect and temple bodies**

[79] Hindu American Foundation, "Can AI-generated images be used in worship?" (Devala Rees) — https://www.hinduamerican.org/?p=25156 — published 6 Oct 2025, updated 24 Oct 2025; read 2026-10-19.
[80] Hindu American Foundation, guidelines on the commercial use of deity images — https://www.hinduamerican.org/?p=2408 — undated; read 2026-10-19 — "don't do it" and "caution" tiers.
[81] Das, Kundu, Mim, Guha and Ahmed, "Generative AI Alignment with Hinduism's Theological Plurality and Sacred Representation", arXiv:2608.28228v1 — https://arxiv.org/html/2608.28228v1 — 28 Aug 2026; read 2026-10-19 — 15 interviews, June 2024 to April 2026; models not named.
[82] Feeza Vasudeva, "The Double Life of the Image: Generative AI and Hindu Visual Culture", University of Zurich Digital Religion(s) blog — https://www.uzh.ch/blog/digitalreligions/2026/08/21/the-double-life-of-the-image-generative-ai-and-hindu-visual-culture/ — 21 Aug 2026; read 2026-10-19.
[83] Sambad English, SJTA files police complaint over AI-generated videos of Lord Jagannath — https://sambadenglish.com/latest-news/sjta-files-police-complaint-over-ai-generated-videos-of-lord-jagannath-11014550 — 20 Jan 2026; read 2026-10-19.
[84] Organiser, AI-generated videos of Bhagwan Jagannath spark outrage — https://organiser.org/2026/01/21/336054/bharat/odisha-ai-generated-videos-of-bhagwan-jagannath-spark-outrage-puri-temple-administration-files-police-complaint/ — 21 Jan 2026; read 2026-10-19 — "nationalist" slant; temple's account only.
[85] IOL, Phoenix artist under fire for AI images with Hindu deities — https://iol.co.za/thepost/news/2024-10-06-phoenix-artist-under-fire-for-ai-images-with-hindu-deities/ — about 2024 (the page says "2 years ago"); read 2026-10-19.
[86] The Star, Tamil Nadu: temples ease phone restrictions, retain ban on photography — https://www.thestar.com.my/aseanplus/aseanplus-news/2026/10/11/tamil-nadu-temples-ease-phone-restrictions-retain-ban-on-photography — 11 Oct 2026; read 2026-10-19.
[87] The Week (wire), TTD warns against filming social media reels in Tirumala — https://www.theweek.in/wire-updates/national/2025/07/31/srg4-ap-ttd-reeels-warning.html — 31 Jul 2025 — digest only.
[88] Hindu American Foundation, Reporters Guide to the Swastika — https://www.hinduamerican.org/swastika-reporters-guide/ — undated; read 2026-10-19 (the 45-degree description is from a WION explainer credited to HAF, digest only: https://embed.wionews.com/web-stories/india-news/business-economy/difference-between-swastika-and-hakenkreuz-1719917836714).
[89] Axios, New ChatGPT update spurs flood of Ghibli-style portraits — https://www.axios.com/2025/03/26/chatgpt-images-ghibli-portraits — 26 Mar 2025 — digest only.
[90] Tilkayat Shri Govindlaji Maharaj v. State of Rajasthan (1963) — https://www.scobserver.in/wp-content/uploads/2026/04/Tilkayat-Shri-Govindlaji-Maharj-v-State-of-Rajasthan-1963.pdf — digest only.

**Exemplars**

[91] Wikipedia, Ramayana: The Legend of Prince Rama — https://en.wikipedia.org/wiki/Ramayana:_The_Legend_of_Prince_Rama — 2026-10-19 (read).
[92] Wikipedia, Sita Sings the Blues — https://en.wikipedia.org/wiki/Sita_Sings_the_Blues — 2026-10-19 (read).
[93] Wikipedia, Adipurush — https://en.wikipedia.org/wiki/Adipurush — 2026-10-19 (read; first 100,000 of 135,700 characters).
[94] Wikipedia, Mahavatar Narsimha — https://en.wikipedia.org/wiki/Mahavatar_Narsimha — 2026-10-19 (read).
[95] Wikipedia, The Legend of Hanuman — https://en.wikipedia.org/wiki/The_Legend_of_Hanuman — 2026-10-19 (read).
[96] Wikipedia, Arjun: The Warrior Prince — https://en.wikipedia.org/wiki/Arjun:_The_Warrior_Prince — 2026-10-19 (read).
[97] Wikipedia, Amar Chitra Katha — https://en.wikipedia.org/wiki/Amar_Chitra_Katha — 2026-10-19 (read).
[98] Wikipedia, Sanjay's Super Team — https://en.wikipedia.org/wiki/Sanjay%27s_Super_Team — 2026-10-19 (read).
[99] Wikipedia, Little Krishna — https://en.wikipedia.org/wiki/Little_Krishna — 2026-10-19 (read).
[100] Wikipedia, Nina Sabnani — https://en.wikipedia.org/wiki/Nina_Sabnani — 2026-10-19 (read).
[101] Bombay Rose — https://www.cartoonbrew.com/feature-film/first-trailer-bombay-rose-an-indian-european-co-production-impresses-at-venice-film-festival-178985.html ; https://www.screendaily.com/reviews/bombay-rose-venice-review/5142095.article — 2026-10-19 — digest only.
[102] Studio Eeksaurus — https://homegrown.co.in/homegrown-creators/the-creative-chaos-of-5-indian-independent-animation-studios ; https://bangaloreinternationalcentre.org/event/eeksaurus-revealed-behind-the-animated-curtain/ — 2026-10-19 — digest only.
[103] Mahavatar Narsimha research and team claims — https://iskconnews.org/the-journey-behind-the-making-of-mahavatar-narasimha-official-trailer-released-today/ ; https://www.hollywoodreporterindia.com/features/interviews/mahavatar-narsimha-director-ashwin-kumar-on-vishnu-anime-and-indian-mythology ; one low-quality site claiming 14 scholars — 2026-10-19 — digest only.

**Phone fixture and commissioning**

[104] Phone-legibility fixture, this sprint — `research/hindu-visual-fixtures/` (chart, results, README) — 2026-10-19 — M-H1.
[105] Anecdotal WhatsApp reports — https://obsproject.com/forum/threads/what%C2%B4s-the-best-video-quality-small-files-for-whatsapp-settings.110051/ ; https://www.guidingtech.com/send-hd-photos-and-videos-in-whatsapp/ — 2026-10-19 — digest only: about 640 px wide at about 500 kb/s, some 15 fps; "HD" means 720p. Not a measurement of the real encoder.
[106] MeMeraki listings (Pattachitra, Tanjore, Madhubani) — https://www.memeraki.com/collections/purusottam-swain/products/jaggannath-in-pattachitra-by-purusottam-swain-2 ; https://www.memeraki.com/products/balaji-in-tanjore-by-sanjay-tandekar — 2026-10-19 — prices and times from search digests; the pages returned HTTP 429.
[107] Exotic India Tanjore painting listings — found by search on 2026-10-19; the US$5,020 and "at least one or two months" figures are from a digest and the individual listing URL was not recorded against the figure.
[108] Pushtimarg devotional page on disposing of sacred images — https://pushti-marg.net/bhagwat/visarjan-2.htm — 2026-10-19 — digest only.

**Project documents used (not numbered)**

`CHARTER.md`; `DECISIONS.md` (D-03, D-04, D-07, D-16, D-27, D-28, D-29; W-23, W-32 to W-34, W-38, W-40, W-46, W-48; O-02, O-06, O-10, O-27, O-43); `reviews/04-hindu-mobile-briefs-review.md`; `playbooks/cinematic-quality.md` (T1 PR2, T2, T5, T6, T9, Exercise 9, Decisions); `playbooks/animated.md` (Decisions 1 and 11, Exercise 7); `playbooks/ai-imagery.md` (Steps 9 and 10); `playbooks/theatrical-delivery.md` (T8, T10); `playbooks/agent-pipeline.md` (Route A, `seekTo(t)`); `playbooks/craft-visual.md` (SVG hooks, `data-pivot`); `playbooks/toolchain.md` (source [66], MDN `stroke-dashoffset`); `research/sources/theatrical-delivery-round2-excerpts-2026-10-18.txt`; `research/hindu-visual-fixtures/README.txt`; `research/sources/hindu-visual-licence-excerpts-2026-10-19.txt`.
