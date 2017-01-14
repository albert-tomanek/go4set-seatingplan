
public class Classroom : Gtk.DrawingArea
{
	public Array <Table> tables = new Array <Table> ();

	private Table? dnd_object    = null;	// The object being dragged
	private int? object_offset_x = null;	// Offset from the object's top left
	private int? object_offset_y = null;


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
					| Gdk.EventMask.POINTER_MOTION_MASK				// For moving dnd real-time
					);

	}

	/* Override methods */

	public override bool button_press_event (Gdk.EventButton event)
	{
		if (event.button == 1)
		{
			/* Left click; start dragging an object */

			this.dnd_object = this.get_object_at((int) event.x, (int) event.y);			// (returns null if no object is found)

			if (this.dnd_object != null)
			{
				this.object_offset_x = (int) event.x - this.dnd_object.x;
				this.object_offset_y = (int) event.y - this.dnd_object.y;
			}
		}
		if (event.button == 3)
		{
			/* Right click to add a table */

			this.add_table(120, 80, (int) event.x, (int) event.y);
		}

		return false;
	}

	public override bool motion_notify_event (Gdk.EventMotion event)
	{
		if (this.dnd_object != null)
		{
			/* Move the object to the current location for real-time dragging */
			this.dnd_object.move((int) event.x - this.object_offset_x, (int) event.y - this.object_offset_y);	// Move the object, with the correct offset of its top left corner

			this.queue_draw();		// Redraw our classroom
		}

		return false;
	}

	public override bool button_release_event (Gdk.EventButton event)
	{
		if (event.button == 1 && this.dnd_object != null)
		{
			/* They've just stopped dragging an object */

			this.dnd_object = null;
			this.object_offset_x = null;
			this.object_offset_y = null;
		}

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

	public Table? get_object_at(int x, int y)
	{
		Table return_table = null;

		for (int i = 0; i < this.tables.length; i++)
		{
			Table table = this.tables.index(i);

			if ( table.x < x && x < (table.x + table.width ) &&
				 table.y < y && y < (table.y + table.height) )
			{
				return_table = table;
			}
		}

		return return_table;
	}
}
