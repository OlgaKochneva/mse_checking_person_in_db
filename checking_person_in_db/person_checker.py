import click

from app import App


@click.command()
@click.option('--source', '-s', required=True, type=str, help='File path or cam id')
@click.option('--skip-frames', '-f', type=int, help='Number of skipped frames')
@click.option('--tolerance', '-t', type=float, help='Comparison accuracy (from 0 to 1)')
@click.option('--upsample-times', '-u', type=int, help='Processing quality')
@click.option('--report/--no-report', is_flag=True, default=True, help='Generate report')
@click.option('--video/--no-video', is_flag=True, help='Generate processed video')
def main(source, skip_frames, tolerance, upsample_times, report, video):
    app = App(source)
    if skip_frames:
        app.face_finder.skip_frames_num = skip_frames
    if tolerance:
        app.face_comparer.tolerance = tolerance
    if upsample_times:
        app.face_finder.upsample_num = upsample_times
    app.face_finder.generate_report = report
    app.face_finder.generate_video = video
    app.run()


if __name__ == '__main__':
    main()
