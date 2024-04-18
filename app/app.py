import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 
from shinywidgets import render_plotly

#The lines below are used to import and change the font

ui.tags.link(
    rel="stylesheet",
    href="https://fonts.googleapis.com/css?family=Roboto"
)

ui.tags.style(
    "body { font-family: 'Roboto', sans-serif; }"
)

#AI is not well versed on coding in Shiny. So, the most useful resource I have found is this website: https://shiny.posit.co/py/

#AI can be useful if you already have some of your code written and are asking it to correct and issue

#It can be frustrating but don't give up. Take a break from the screen if you're getting hung up on something. The frustration will only make it harder to think clearer and find a solution. 

#Don't forget that even the smallest mistake can throw off the whole code: incorrect indentation, missing punctuation, incorrect capitalization, etc. 



df = palmerpenguins.load_penguins()

ui.page_opts(title="Penguins dashboard", fillable=True)


with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )


with ui.layout_column_wrap(fill=False):
    with ui.value_box(showcase=icon_svg("earlybirds"), style="color:blue"):
        "Number of penguins"

        @render.text
        def count():
            return filtered_df().shape[0]

    with ui.value_box(showcase=icon_svg("ruler-horizontal"), style="color:blue"):
        "Average bill length"

        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    with ui.value_box(showcase=icon_svg("ruler-vertical"), style="color:blue"):
        "Average bill depth"

        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"



    with ui.card(full_screen=True):
        ui.card_header("Penguin data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)

ui.input_selectize(
    "var", "Select variable",
    choices=["bill_length_mm", "body_mass_g"]
)

@render_plotly
def hist():
    import plotly.express as px
    from palmerpenguins import load_penguins
    df = load_penguins()
    return px.histogram(df, x=input.var())


#ui.include_css(app_dir / "styles.css")


@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
