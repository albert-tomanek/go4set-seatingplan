/* Compile: valac main.vala classroom.vala --pkg gtk+-3.0 */

public class SeatingPlanApp : Gtk.Application
{
	protected override void activate ()
	{
		var root = new Gtk.ApplicationWindow(this);
		root.title = "Seating Plan";
		root.set_border_width(12);
		root.destroy.connect(Gtk.main_quit);

		var grid = new Gtk.Grid();
		root.add(grid);

		/* Make our classroom area */
		var classroom = new Classroom();
		classroom.set_size_request(640, 480);					// Thank you Jens Mühlenhoff [ http://stackoverflow.com/questions/40775041/gtk-drawingarea-blank-when-attached-to-gtk-grid ]
		grid.attach(classroom, 0, 0, 1, 1);						// The grid's 8 cells high for now

		/* Make a separate grid for controls */
		var controlsGrid = new Gtk.Grid();
		grid.attach(controlsGrid, 1, 0, 1, 1);

		/* Add a 'New Table' button */
		var newTableButton = new Gtk.Button.with_label("New Table");
		newTableButton.clicked.connect( () => {print("new table button clicked\n"); classroom.new_table_popup( newTableButton ); } );
		controlsGrid.attach(newTableButton, 0, 0, 1, 1);

		root.show_all();
	}

	public SeatingPlanApp()
	{
		Object(application_id : "com.github.albert-tomanek.SeatingPlan");
	}
}

int main (string[] args)
{
	return new SeatingPlanApp().run(args);
}
