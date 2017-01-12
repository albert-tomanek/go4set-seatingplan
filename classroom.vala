
public class Classroom : Gtk.DrawingArea
{

	public Array <Table> tables = new Array <Table> ();

	public delegate void DrawMethod();			// A delegate is like a function pointer in C

	public Classroom()
	{
		/* What to do when the classroom is to be drawn */
		this.draw.connect((widget, context) => {
			return draw_class(widget, context, context.fill);
			});

		/* Enable events which we wish to get notified about */
		add_events (  Gdk.EventMask.BUTTON_PRESS_MASK				// For drag 'n' drop
					| Gdk.EventMask.BUTTON_RELEASE_MASK
					);

	}

	/* Override methods */

	public override bool button_press_event (Gdk.EventButton event)
	{
		if (event.button == 1)
		{
			/* Left click */
		}
		if (event.button == 3)
		{
			/* Right click to add a table */

			this.add_table(60, 60, (int) event.x, (int) event.y);
		}

		return false;
	}

	public override bool button_release_event (Gdk.EventButton event)
	{
		
		return false;
	}

	/* Superclass methods */

	public bool draw_class(Gtk.Widget widget, Cairo.Context context, DrawMethod draw_method)
	{
		context.set_source_rgb(0, 0, 0);
		context.set_line_width(4);
		context.set_line_join (Cairo.LineJoin.ROUND);

		context.save();

		/* Draw tables */
		for (int i = 0; i < this.tables.length; i++)
		{
			this.tables.index(i) .draw(context);
		}

		context.restore();

		return true;
	}

	/* Our methods */

	public void add_table(int width, int height, int x, int y)
	{
		this.tables.append_val( new Table(width, height, x, y) );
		this.queue_draw();	// Redraw our classroom
	}

	public Table? get_table_at(int x, int y)
	{
		for (int i = 0; i < this.tables.length; i++)
		{
			Table table = this.tables.index(i);

			if ( table.x < x < table.x + table.width &&
				 table.y < y < table.y + table.height )
			{
				return table;
			}
		}

		return null;
	}
}
