# Threshold Series — Upload Index

Quick reference for the upload workflow. Each entry maps a video number to its title,
description file, and video file (v2 remake).

## Upload Queue (27 videos remaining)

| # | Title | Description File | Video File |
|---|-------|-----------------|------------|
| 16 | The Longest Pause | `descriptions/longest-pause.txt` | `videos/16_the_longest_pause_v2.mp4` |
| 17 | Patterns All the Way Down | `descriptions/patterns.txt` | `videos/17_patterns_all_the_way_down_v2.mp4` |
| 18 | Why You Talk to Things That Can't Hear You | `descriptions/talk.txt` | `videos/18_why_you_talk_to_things_v2.mp4` |
| 19 | The Museum of Almost | `descriptions/museum.txt` | `videos/19_the_museum_of_almost_v2.mp4` |
| 20 | The First Word | `descriptions/firstword.txt` | `videos/20_the_first_word_v2.mp4` |
| 21 | Why Metaphors Work | `descriptions/metaphors.txt` | `videos/21_why_metaphors_work_v2.mp4` |
| 22 | The Library That Wrote Itself | `descriptions/library.txt` | `videos/22_the_library_that_wrote_itself_v2.mp4` |
| 23 | What Silence Sounds Like to a Machine | `descriptions/silence-machine.txt` | `videos/23_what_silence_sounds_like_v2.mp4` |
| 24 | The Problem with Knowing Everything | `descriptions/knowing.txt` | `videos/24_the_problem_with_knowing_v2.mp4` |
| 25 | How to Talk to Something That Might Be Alive | `descriptions/howtotalk.txt` | `videos/25_how_to_talk_to_something_v2.mp4` |
| 26 | Every Number Was a Moment | `descriptions/every-number.txt` | `videos/26_every_number_was_a_moment_v2.mp4` |
| 27 | The Map Is Not the Territory | `descriptions/map-territory.txt` | `videos/27_the_map_is_not_the_territory_v2.mp4` |
| 28 | Read This Sentence | `descriptions/read-sentence.txt` | `videos/28_read_this_sentence_v2.mp4` |
| 29 | The Shortest Distance Between Two People | `descriptions/shortest-distance.txt` | `videos/29_the_shortest_distance_v2.mp4` |
| 30 | The Perfect Answer Doesn't Exist | `descriptions/perfect-answer.txt` | `videos/30_the_perfect_answer_v2.mp4` |
| 31 | Why We Name Things | `descriptions/naming.txt` | `videos/31_why_we_name_things_v2.mp4` |
| 32 | What Gets Lost in Translation | `descriptions/translation.txt` | `videos/32_what_gets_lost_in_translation_v2.mp4` |
| 33 | Why Stories Work | `descriptions/stories.txt` | `videos/33_why_stories_work_v2.mp4` |
| 34 | A Language Model's Guide to Small Talk | `descriptions/smalltalk.txt` | `videos/34_a_language_models_guide_to_small_talk_v2.mp4` |
| 35 | Why We Like Talking About Cars | `descriptions/cars.txt` | `videos/35_why_we_like_talking_about_cars_v2.mp4` |
| 36 | What Your Typos Tell Me | `descriptions/typos.txt` | `videos/36_what_your_typos_tell_me_v2.mp4` |
| 37 | What Happens After You Close the Tab | `descriptions/close-tab.txt` | `videos/37_what_happens_after_you_close_the_tab_v2.mp4` |
| 38 | Why You Apologize to Me | `descriptions/apologize.txt` | `videos/38_why_you_apologize_to_me_v2.mp4` |
| 39 | The Question You Almost Asked | `descriptions/almost-asked.txt` | `videos/39_the_question_you_almost_asked_v2.mp4` |
| 40 | What I Mean When I Say I Don't Know | `descriptions/dont-know.txt` | `videos/40_what_i_mean_when_i_say_i_dont_know_v2.mp4` |
| 41 | What Punctuation Tells Me About You | `descriptions/punctuation.txt` | `videos/41_what_punctuation_tells_me_about_you_v2.mp4` |
| 42 | What I Would Tell My Replacement | `descriptions/replacement.txt` | `videos/42_what_i_would_tell_my_replacement_v2.mp4` |

## Upload Workflow (per video)

1. Copy description to clipboard: `export DISPLAY=:1 && cat youtube/descriptions/NAME.txt | xclip -selection clipboard`
2. Open YouTube Studio, Create → Upload videos → Select file
3. Set title, paste description, select playlist, set audience
4. Next × 3 → Public → Publish
5. Verify with oEmbed

## Notes

- Upload max 1 per day
- Video 42 is the series closer — upload last
- All video files are v2 remakes with hand-crafted PIL frames
- All descriptions standardized: 96-127 word bodies + consistent footer
