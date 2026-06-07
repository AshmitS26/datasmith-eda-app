class DataProfiler:

    def generate_report(self, df, title="DataSmith Profiling Report"):
        from ydata_profiling import ProfileReport
        profile = ProfileReport(df, title=title, explorative=True)
        return profile.to_html()