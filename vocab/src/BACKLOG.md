# Vocabulary backlog

Terms sketched but not yet entered in the SKOS Editor. Rescued from
`vocab/index.md` when that page became generated output — of the 174 names
below, 98 already exist in the vocabulary and 76 do not.

Not published: `vocab/src/` is in the Jekyll `exclude:` list. Tracked in git so
the design work survives.

Notation carried over from the original sketch: `bt::` broader term, `rt::`
related term, `at::` alternative label, `cm::` close match. `(proposed)` marks a
term that had not been created yet; `*` marked names that needed a decision.

---

## Terms

- [`pkm:taxonomy`](pkm_taxonomy.ttl)

  - [`pkmv:Meal`](pkmv_Meal.ttl) 
    rt::MealPlan 
    - [`pkmv:Recipe`](Recipe.ttl) 
      rt::MealPlan cm::schema.org/Recipe
      - [`pkmv:DayMeal`](pkmv_DayMeal.ttl)
      rt::MealPlan
        - [`pkmv:DayCluster`](pkmv_DayCluster.ttl) 
          rt::MealPlan
          - [`pkmv:DayMealPlan`](pkmv_DayMealPlan.ttl) 
            rt::DayMealPlan
            - [`pkmv:DayMeal`](pkmv_DayMeal.ttl) 
            rt::MealPlan
              - [`pkmv:Breakfast`](pkmv_Breakfast.ttl) 
              bt::DayMeal 
              rt::MealPlan 
              cm::schema.org/Recipe
              - [`pkmv:Lunch`](pkmv_Lunch.ttl) 
              bt::DayMeal
              rt::MealPlan 
              cm::schema.org/Recipe
              - [`pkmv:Dinner`](pkmv_Dinner.ttl)
              at::Supper
              bt::DayMeal
              rt::MealPlan 
              cm::schema.org/Recipe
                - [`pkmv:Snack`](pkmv_Snack.ttl) 
                bt::DayMeal 
                rt::MealPlan 
                cm::schema.org/Recipe
  
  - [`:taxonomy`](pkm_taxonomy.ttl)
    - :MealPlan
      :MealPlan2
      - [`:Meal`](pkmv_Meal.ttl) 

        - [`:DayMealPlan`](pkmv_DayMealPlan.ttl) 
          - [`:DayMeal`](pkmv_DayMeal.ttl)
            - [`:Breakfast`](pkmv_Breakfast.ttl)
            - [`:Lunch`](pkmv_Lunch.ttl)
            - [`:Dinner`](pkmv_Dinner.ttl)
            at::Supper
            - [`:Snack`](pkmv_Snack.ttl)
        
          - [`:Recipe`](Recipe.ttl) 
            cm::schema.org/Recipe
            - :RecipeTime
            - :RecipeServings
            - :RecipeSource
            - :RecipeImages
            - :Nutrition
            - :Ingredient
            :Recipe2

            

  :Food
  :Package
  :Restaurant
  :Menu
  

  
  :Glossary (proposed)
    :Term
  : Vocabulary (proposed)
    :Concept
  :Taxonomy
    :Relation (proposed)

  :Ontology
    :Metadata
      :Properties (proposed)
        :Property (proposed)

  :KnowledgeGraph
    :Node (proposed)
    :Relationship (proposed) at::Edge at::Relation
    :Property (proposed)

  :Cluster
    ConceptCluster (proposed)
    :EffortCluster (proposed)
    :TopicCluster (proposed)
    :OutputCluster (proposed)

  :Standard
    :SKOS
    :RDF
    :OWL

  :Add
    :Draft
    :Clipping
    :Spark
    :Idea
    :Focus

  :Atlas
    :Knowledge
      :Topic

  :Calendar
    :Time
      :Day
        - [`:DayCluster`](pkmv_DayCluster.ttl)
          :DayIndex
          :DayPlan
          :DaySchedule
          :DayLog
          :DayJournal
          :DayReview
          :DayAnalysis
          :DayLinks
          :DayActions
          :DayHealth
          :DayDiabetes
          :DayDiabetesAnalysis


    :Week
      :WeekCluster
      :WeekIndex
      :WeekPlan
      :WeekLog
      :WeekJournal
      :WeekReview
      :WeekAnalysis
      :WeekHealth
      :WeekMealPlan
      :WeekDiabetes
      :WeekDiabetesAnalysis

      :Month

      :Quarter

      :Year

      :Decade

      :Life
  
  :Calendar2  


  :Effort
    :Action
    :Area
    :Interest
    :Project
    :Sprint (proposed)
  :Effort2

  :Extra
    :Template
    :Script

  :Tool

  :App (proposed)

  :Database (proposed)
    :Neo4j
      :Cypher

  :Language (proposed)
    :Python
      :FastAPI
    :Swift
      :AppIntent
      :Hummingbird

  :Platform (proposed)
    :macOS (proposed)
    :iOS (proposed)
    :watchOS (proposed)
    :tvOS (proposed)

  :Technology (proposed)
    :AppleFramework (proposed)
      :SwiftFramework (proposed)
        :AppIntent
      :SwiftPackage (proposed)
        :Hummingbird
    :AppleApp (proposed)
      :Shortcuts (proposed)
        :Shortcut
      :Siri

  :Obsidian
  :Obsidian2
    :Vault*
      :Folder* (proposed)
        :File* (proposed)
          :MarkdownFile (proposed)
          :CanvasFile (proposed)
          :DrawingFile (proposed)
          :BaseFile (proposed)
          :ViewFile (proposed)
          :BoardFile (proposed)
          :MindmapFile (proposed)
          :MermaidFile (proposed)
          :ImageFile (proposed)
          :TextFile (proposed)
          :DocumentFile (proposed)
          :CsvFile (proposed)
          :JsonDFile (proposed)
          :OtherFile (proposed)
        :Folder* (proposed)
          :File* (proposed)
 
    :Event (proposed)
        :PKMEvent (proposed)
            :HealthEvent (proposed)
                :DiabetesEvent (proposed)
                    :GlucoseEvent (proposed)
                    :InsulinEvent (proposed)
                    :MealEvent (proposed)
                    :ActivityEvent (proposed)
                    :NoteEvent (proposed)
                    :FoodEvent (proposed)
                    :CalibrationEvent (proposed)
  :Error (proposed)
    :PKMError (proposed)
      :HealthError (proposed)
        :DiabetesError (proposed)
          :GlucoseError (proposed)
          :InsulinError (proposed)
          :MealError (proposed)
          :ActivityError (proposed)
          :NoteError (proposed)
          :FoodError (proposed)
          :CalibrationError (proposed)
  :Alert (proposed)
    :PKMAlert (proposed)
      :HealthAlert (proposed)
        :DiabetesAlert (proposed)
          :GlucoseAlert (proposed)
          :InsulinAlert (proposed)
          :ActivityAlert (proposed)
          :MealAlert (proposed)
          :CalibrationAlert (proposed)


