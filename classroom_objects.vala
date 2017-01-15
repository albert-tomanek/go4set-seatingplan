
public class Table : GLib.Object
{
	public int width;
	public int height;
	public int x;
	public int y;

	public Table(int width, int height, int x = 0, int y = 0)
	{
		this.width  = width;
		this.height = height;
		this.x = x;
		this.y = y;
	}

	public void move(int x, int y)
	{
		this.x = x;
		this.y = y;
	}

	public delegate void DrawMethod();

	public void draw(Cairo.Context context)
	{
			context.set_source_rgb((1.0/256.0) * 55.0, (1.0/256.0) * 110.0, (1.0/256.0) * 180.0);		// Fill the area with blue (55, 110, 180)
			__draw(context, context.fill);

			context.set_source_rgb(0, 0, 0);	// Draw a border in black
			__draw(context, context.stroke);
	}

	private void __draw(Cairo.Context context, DrawMethod draw_method)
	{
		context.new_path();
		context.move_to(this.x, this.y);
		context.rel_line_to(width, 0);
		context.rel_line_to(0, height);
		context.rel_line_to(-width, 0);
		context.rel_line_to(0, -height);
		context.close_path();

		draw_method();
	}
}
