#!/bin/bash

sqlite3 ~/.local/share/liferea/liferea.db \
".mode column" \
".headers on" \
"SELECT datetime(date, 'unixepoch') AS date, n.title AS source, i.title FROM items i INNER JOIN node n ON n.node_id = i.node_id AND i.read = 0 AND i.parent_item_id = 0 ORDER BY date ASC;" \
".q"

echo -e "\nThat's all."

