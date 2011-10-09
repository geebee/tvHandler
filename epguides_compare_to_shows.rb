#!/usr/bin/env ruby

require 'optparse'
require 'rubygems'
require 'nokogiri'
require 'open-uri'
require 'htmlentities'

options = {}

optparse = OptionParser.new do |opts|
    opts.banner = "Usage: ./epguides_compare_to_shows.rb --tv-folder/-f <directory> --title/-t <show title> ..."

    options[:folder] = "/media/tv"
    opts.on("-f", "--tv-folder FOLDER", "Top-Level directory containing the shows to compare") do |folder|
        options[:folder] = folder
    end

    options[:title] = ""
    opts.on("-t", "--title TITLE", "Title of the show to compare") do |title|
        options[:title] = title
    end

    opts.on("-h", "--help", "Display this help screen") do
        puts opts
        exit
    end
end

optparse.parse!

tvLocation = "#{options[:folder]}"
showTitle = "#{options[:title]}"

if showTitle == ""
    puts "-t/--title <show title> is a required parameter."
    exit
end

puts "Using Directory: #{tvLocation}"
puts "Show Title: #{showTitle}"

epguidesTitle = showTitle.split(" ").join()
epguidesURL = "http://epguides.com/#{epguidesTitle}/"

escapeHtmlEntities = HTMLEntities.new
preShowPage = Nokogiri::HTML(open(epguidesURL)).to_html.gsub!("\n","")
showPage = escapeHtmlEntities.decode(preShowPage)
showHashArray = Array.new
showPage.scan(/\d+. +(\d+) *\- *(\d+).*?<a.*?>(.*?)<\/a>/) do |season, episode, title|
    #puts "Season: #{season}, Episode: #{episode} - Title: #{title}"
    tempEpisodeHash = Hash.new

    tempEpisodeHash[:season] = season
    tempEpisodeHash[:episode] = episode
    tempEpisodeHash[:title] = title 

    tempEpisodeHash[:file_name] = "#{showTitle} - S"
    if tempEpisodeHash[:season].to_i < 10
        tempEpisodeHash[:file_name] += "0#{tempEpisodeHash[:season]}"
    else
        tempEpisodeHash[:file_name] += "#{tempEpisodeHash[:season]}"
    end
    
    tempEpisodeHash[:file_name] += "E#{tempEpisodeHash[:episode]}"
    #
    # Put no file extension on the 'file_name' attribute' for matching below
    tempEpisodeHash[:file_name] += " - #{tempEpisodeHash[:title]}"

    showHashArray.push(tempEpisodeHash)
end

#puts "#{tvLocation}/#{showTitle}/Season #{showHashArray[0][:season]}/#{showHashArray[0][:file_name]}"

showHashArray.each_with_index do |ep, i|
    if File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:file_name]}.avi")\
    or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:file_name]}.mkv")\
    or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:file_name]}.mpg")\
    or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:file_name]}.mp4")\
    or File.exists?("#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:file_name]}.m4v")
        #puts "Exists"
    else
        puts "#{tvLocation}/#{showTitle}/Season #{ep[:season]}/#{ep[:file_name]}"
    end
end
