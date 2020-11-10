<template>
    <div>
    <v-navigation-drawer app>
        <v-list-item v-for="s in slides" :key="s.message" link @click.stop="update_slide">
            <v-list-item-content>
                <slide :message="s.message"> </slide>
            </v-list-item-content>
        </v-list-item>
    </v-navigation-drawer>

    <v-app-bar app>

        <v-toolbar-title>Huddle</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" id="text_box">
                    <!-- <v-icon>mdi-vector-square</v-icon> -->
                </v-btn>
             </template>
             <span>New Textbox</span>
        </v-tooltip>
        <v-tooltip bottom>
             <template v-slot:activator="{ on, attrs }">
                <v-btn icon v-bind="attrs" v-on="on" @click.stop="append_slide">
                    <v-icon>mdi-plus</v-icon>
                </v-btn>
             </template>
             <span>New Slide</span>
        </v-tooltip>
    </v-app-bar>

    <div class="pa-5">
        <v-fade-transition appear>
            <v-card width=125vh height=70.3125vh>
                <div id="graph-wrapper"></div>
            </v-card>
        </v-fade-transition>
    </div>

    </div>
</template>

<script>
import Slide from '@/components/app/Slide';
import {mapState} from 'vuex';

var graph;

export default {
    name: 'Workspace',
    data() {
        return {
            curr_slide_id: 0,
            slides: [
                { message: 'Yo' }
            ]
        }
    },
    mounted() {
        this.draw();
    },
    updated() {
        console.log(document.body.getElementsByTagName("graph-wrapper"));
        this.slides[this.curr_slide_id].message = document.body.getElementsByTagName("graph-wrapper");
    },
    methods:
    {
        update_slide() {
            console.log(this.slides);
            console.log(this.curr_slide_id);
        },
        append_slide() {
            this.slides.push({ message: this.slides.length });
            console.log(this.slides);
            console.log(this.curr_slide_id);
        },
        draw()
        {
            if (!mxClient.isBrowserSupported()) {
                mxUtils.error("Browser is not supported!", 200, false);
            } else {
                mxPanningHandler.prototype.isPanningEnabled = function(value) {
                    return false;
                };
                mxConnectionHandler.prototype.connectImage = new mxImage(
                "images/connector.gif",
                16,
                16
                );

                // new toolbar without event processing
                var toolbar = new mxToolbar(document.getElementById("text_box"));
                toolbar.enabled = false;

                // the div for the graph
                var container = document.createElement("div");   
                container.id = "grid" // KS: add an Id so we can find it later
                container.style.position = "absolute";
                container.style.overflow = "hidden";
                container.style.left = "0px";
                container.style.top = "0px";
                container.style.right = "0px";
                container.style.bottom = "0px";
                container.style.background =
                'url("https://jgraph.github.io/mxgraph/javascript/examples/editors/images/grid.gif")';

                // add drag/drop events to grid
                container.addEventListener("dragover", function(event) {
                    event.preventDefault();
                });
                
                // add drag/drop events to grid
                container.addEventListener("drop", function(event) {
                    drop(event);
                });

                document.getElementById("graph-wrapper").appendChild(container);

                // workaround for Internet Explorer ignoring certain styles
                if (mxClient.IS_QUIRKS) {
                    document.body.style.overflow = "hidden";
                    new mxDivResizer(tbContainer);
                    new mxDivResizer(container);
                }

                // creates the model and the graph inside the container
                var model = new mxGraphModel();
                graph = new mxGraph(container, model);

                graph.setConnectable(false);
                graph.setMultigraph(false);

                // stops editing on enter or escape keypress
                var keyHandler = new mxKeyHandler(graph);
                var rubberband = new mxRubberband(graph);

                var addVertex = function(icon, w, h, style) {
                var vertex = new mxCell(null, new mxGeometry(0, 0, w, h), style);
                vertex.setVertex(true);

                console.log("vertex vertex", vertex);

                var funct = function(graph, evt, cell, x, y) {
                    graph.stopEditing(false);

                    var v = graph.getModel().cloneCell(vertex);
                    v.geometry.x = x;
                    v.geometry.y = y;

                    graph.addCell(v);
                    graph.setSelectionCell(v);
                };

                // Creates the image which is used as the drag icon (preview)
                var img = toolbar.addMode(null, icon, function(evt, cell) {
                    var pt = this.graph.getPointForEvent(evt);
                    funct(graph, evt, cell, pt.x, pt.y);
                });

                mxEvent.addListener(img, "mousedown", function(evt) {
                    // do nothing
                });

                mxEvent.addListener(img, "mousedown", function(evt) {
                    if (img.enabled == false) {
                    mxEvent.consume(evt);
                    }
                });

                mxUtils.makeDraggable(img, graph, funct);
                //img.enabled = true;

                graph.getSelectionModel().addListener(mxEvent.CHANGE, function() {
                    var tmp = graph.isSelectionEmpty();
                    mxUtils.setOpacity(img, tmp ? 100 : 20);
                    img.enabled = tmp;
                });
                };

                addVertex("https://jgraph.github.io/mxgraph/javascript/examples/editors/images/rounded.gif", 100, 40, "shape=rounded");
            }
        },
        
        drag(ev) {
            ev.dataTransfer.setData("text", ev.target.innerText);
        },

        drop(ev) {
            ev.preventDefault();
            
            var data = ev.dataTransfer.getData("text");
            var parent = graph.getDefaultParent();
            graph.getModel().beginUpdate();
            
                var gridRect = $('#grid')[0].getBoundingClientRect();
                var targetX = ev.x - gridRect.x;
                var targetY = ev.y - gridRect.y;

            try {
                var v1 = graph.insertVertex(parent, null, data, targetX, targetY, 300, 30);
            } finally {
                graph.getModel().endUpdate();
            }
        }   
    },
    components: {
        Slide
    },
    computed: {
        ...mapState(['workspace'])
    }
}
</script>
