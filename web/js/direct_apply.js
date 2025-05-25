// This script can be run directly in the browser console to test node styling
// It will immediately apply custom colors to all Creepynodes

(function() {
    // Define our colors
    const backgroundColor = "#0b500b";  // Grren background
    const titleColor = "#500b50";       // Dark blue title
    const textColor = "#0b6f0b";        // Light Green text (was white)

    // Get all nodes in the graph
    const nodes = app.graph._nodes;
    let count = 0;

    // Loop through all nodes
    for (let i = 0; i < nodes.length; i++) {
        const node = nodes[i];

        // Check if this is a StarNode (category starts with Creepybits)
        if (node.category && node.category.startsWith("Creepybits")) {
            // Apply custom colors
            node.bgcolor = backgroundColor;
            node.color = textColor;

            // Store the original drawTitleBar function if not already stored
            if (!node._originalDrawTitleBar) {
                node._originalDrawTitleBar = node.drawTitleBar;

                // Override the drawTitleBar function to use our custom title color
                node.drawTitleBar = function(ctx, title_height) {
                    // Call the original function first
                    this._originalDrawTitleBar.call(this, ctx, title_height);

                    // Draw the title text with our custom color
                    if (this.flags.collapsed) {
                        return;
                    }

                    ctx.font = this.title_font || LiteGraph.DEFAULT_TITLE_FONT;
                    const title = this.getTitle();
                    if (title) {
                        // Save context
                        ctx.save();
                        // Set our custom title color
                        ctx.fillStyle = titleColor;
                        // Draw the title text
                        ctx.fillText(title, 10, title_height * 0.75);
                        // Restore context
                        ctx.restore();
                    }
                };
            }

            count++;
        }
    }

    // Force canvas redraw
    app.canvas.setDirty(true);
    app.canvas.draw(true, true);

    // Display a message
    console.log(`Applied custom colors to ${count} Creepynodes`);

    // Add a message to the UI
    const message = document.createElement("div");
    message.style.position = "fixed";
    message.style.top = "10px";
    message.style.left = "50%";
    message.style.transform = "translateX(-50%)";
    message.style.backgroundColor = backgroundColor;
    message.style.color = textColor;
    message.style.padding = "10px";
    message.style.borderRadius = "5px";
    message.style.zIndex = "9999";
    message.style.fontWeight = "bold";
    message.textContent = `Applied custom colors to ${count} Creepynodes`;

    document.body.appendChild(message);

    // Remove the message after 3 seconds
    setTimeout(() => {
        document.body.removeChild(message);
    }, 3000);

    // Also set up a hook for new nodes
    const originalAddNodeMethod = LGraphCanvas.prototype.processContextMenu;
    if (!LGraphCanvas.prototype._customColorsHooked) {
        LGraphCanvas.prototype._customColorsHooked = true;

        LGraphCanvas.prototype.processContextMenu = function(node, event) {
            const result = originalAddNodeMethod.apply(this, arguments);

            // After a small delay to let the node be created
            setTimeout(() => {
                const nodes = app.graph._nodes;
                for (let i = 0; i < nodes.length; i++) {
                    const node = nodes[i];
                    if (node.category && node.category.startsWith("Creepybits") && node.bgcolor !== backgroundColor) {
                        node.bgcolor = backgroundColor;
                        node.color = textColor;
                        app.canvas.setDirty(true);
                    }
                }
            }, 100);

            return result;
        };
    }

    return `Applied custom colors to ${count} Creepynodes. New nodes will also be styled automatically.`;
})();
