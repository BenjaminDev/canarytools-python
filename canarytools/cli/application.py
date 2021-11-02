#  type: ignore
import os

import typer
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from textual import events
from textual.app import App, RenderableType
from textual.widgets import Button, Footer, Header, Placeholder, ScrollView

from canarytools.console import Console
from canarytools.executors import T
from canarytools.models.base import MFlocksSummary, QDevices, Query


class CanaryHeader(Header):
    def render(self) -> RenderableType:
        header_table = Table.grid(padding=(0, 1), expand=True)
        header_table.style = self.style
        header_table.add_column(justify="left", ratio=0, width=8)
        header_table.add_column("title", justify="center", ratio=1)
        header_table.add_column("clock", justify="right", width=8)
        header_table.add_row(
            "🦜", self.full_title, self.get_clock() if self.clock else ""
        )
        header: RenderableType
        header = Panel(header_table, style=self.style) if self.tall else header_table
        return header


class StatsApp(App):
    """An example of a very simple Textual App
        FLOCK_STATS = lambda: {
        'name': '',
        'live': 0,
        'dead': 0,
        'total_tokens': 0,
        'enabled_tokens': 0,
        'disabled_tokens': 0,
        'week_unack': 0,
        'week_ack': 0,
        'weekly_total': 0,
        'completed_updates_total': 0,
        'pending_updates_total': 0,
        'week_unacked_incidents': [],
        'week_acked_incidents': []
    }

    """

    async def on_load(self, event: events.Load) -> None:
        """Bind keys with the app loads (but before entering application mode)"""
        # await self.bind("b", "view.toggle('sidebar')", "Toggle sidebar")

        await self.bind("q", "quit", "Quit")
        self.canaryconsole = Console(
            console_hash="116482ad", api_key=os.environ["API_KEY"]
        )
        # devices = console.devices.all(query=QDevices())

    async def on_mount(self, event: events.Mount) -> None:
        body = ScrollView(gutter=1)
        metrics = ScrollView(gutter=1)
        # Header / footer / dock
        await self.view.dock(CanaryHeader(style="Green"), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        # await self.view.dock(metrics, edge="left", size=30, name="sidebar")

        await self.view.dock(body, edge="top")

        async def get_incidents() -> None:
            flocks_summary: MFlocksSummary = self.canaryconsole.flocks.summaries()
            flock_ids = list(flocks_summary.flocks_summary.keys())
            md_summary = []
            for flock_id in flock_ids:
                name = flocks_summary.flocks_summary[flock_id]["name"]
                offline = flocks_summary.flocks_summary[flock_id]["offline_devices"]
                online = flocks_summary.flocks_summary[flock_id]["online_devices"]
                enabled_tokens = flocks_summary.flocks_summary[flock_id][
                    "enabled_tokens"
                ]
                disabled_tokens = flocks_summary.flocks_summary[flock_id][
                    "disabled_tokens"
                ]

                details = f"# {name}\n__online__: {online}\n__offline__: {offline}\n__enabled_tokens__: {enabled_tokens}\n__disabled tokens__: {disabled_tokens}"
                md_summary.append(details)

            await body.update(Markdown("\n".join(md_summary)))

        await self.call_later(get_incidents)


app = typer.Typer()


@app.command()
def stats():
    StatsApp.run(title="Canary Stats")



def main():
    app()


if __name__ == "__main__":
    SystemExit(main())
